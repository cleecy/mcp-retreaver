"""LLM provider abstraction — ABC + Anthropic, OpenAI, and Google implementations."""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger(__name__)

from mcp import types as mcp_types


# ---------------------------------------------------------------------------
# Shared data types
# ---------------------------------------------------------------------------

Message = dict[str, Any]


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    text: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Abstract provider
# ---------------------------------------------------------------------------


class LLMProvider(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        tools: list[mcp_types.Tool],
        system_prompt: str,
    ) -> LLMResponse:
        """Send a chat completion request and return an LLMResponse."""


# ---------------------------------------------------------------------------
# Anthropic implementation
# ---------------------------------------------------------------------------


def _mcp_tool_to_anthropic(tool: mcp_types.Tool) -> dict[str, Any]:
    """Convert an MCP Tool to the Anthropic tool-use format."""
    return {
        "name": tool.name,
        "description": tool.description or "",
        "input_schema": tool.inputSchema,
    }


def _messages_to_anthropic(messages: list[Message]) -> list[dict[str, Any]]:
    """Convert our generic message list into Anthropic's content-block format.

    Each message in our list is already a dict with ``role`` and ``content``.
    ``content`` may be:
      - a plain string  (user or assistant text)
      - a list of content blocks (tool_use / tool_result blocks)
    """
    out: list[dict[str, Any]] = []
    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        # Collapse consecutive same-role messages (shouldn't happen, but safe)
        if out and out[-1]["role"] == role and isinstance(content, str) and isinstance(out[-1]["content"], str):
            out[-1]["content"] += "\n" + content
        else:
            out.append({"role": role, "content": content})
    return out


class AnthropicProvider(LLMProvider):
    """LLM provider backed by Anthropic's Messages API."""

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str | None = None) -> None:
        # Lazy import so the package is only needed when this provider is used.
        from anthropic import AsyncAnthropic

        self.model = model
        self._client = AsyncAnthropic(api_key=api_key)  # reads ANTHROPIC_API_KEY if None

    async def complete(
        self,
        messages: list[Message],
        tools: list[mcp_types.Tool],
        system_prompt: str,
    ) -> LLMResponse:
        api_tools = [_mcp_tool_to_anthropic(t) for t in tools]
        api_messages = _messages_to_anthropic(messages)

        log.debug(
            "Anthropic API request:\n%s",
            json.dumps(
                {"model": self.model, "system": system_prompt, "messages": api_messages, "tools": api_tools},
                indent=2, default=str,
            ),
        )

        response = await self._client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=api_messages,
            tools=api_tools if api_tools else [],
        )

        log.debug(
            "Anthropic API response:\n%s",
            json.dumps(response.model_dump(), indent=2, default=str),
        )

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input if isinstance(block.input, dict) else json.loads(block.input),
                    )
                )

        return LLMResponse(
            text="\n".join(text_parts) if text_parts else None,
            tool_calls=tool_calls,
        )


# ---------------------------------------------------------------------------
# OpenAI implementation
# ---------------------------------------------------------------------------


def _mcp_tool_to_openai(tool: mcp_types.Tool) -> dict[str, Any]:
    """Convert an MCP Tool to the OpenAI function-calling format."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema,
        },
    }


def _messages_to_openai(messages: list[Message], system_prompt: str) -> list[dict[str, Any]]:
    """Convert our generic message list into OpenAI's chat format.

    Handles translation from Anthropic-style content blocks (tool_use /
    tool_result) into OpenAI's assistant tool_calls + role=tool messages.
    """
    out: list[dict[str, Any]] = [{"role": "system", "content": system_prompt}]

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        if isinstance(content, str):
            out.append({"role": role, "content": content})
            continue

        # content is a list of blocks
        if role == "assistant":
            # Extract text and tool_use blocks
            text_parts: list[str] = []
            tool_calls: list[dict[str, Any]] = []
            for block in content:
                if block.get("type") == "text":
                    text_parts.append(block["text"])
                elif block.get("type") == "tool_use":
                    tool_calls.append({
                        "id": block["id"],
                        "type": "function",
                        "function": {
                            "name": block["name"],
                            "arguments": json.dumps(block["input"]),
                        },
                    })
            assistant_msg: dict[str, Any] = {
                "role": "assistant",
                "content": "\n".join(text_parts) if text_parts else None,
            }
            if tool_calls:
                assistant_msg["tool_calls"] = tool_calls
            out.append(assistant_msg)

        elif role == "user":
            # Could be tool_result blocks or mixed content
            for block in content:
                if block.get("type") == "tool_result":
                    out.append({
                        "role": "tool",
                        "tool_call_id": block["tool_use_id"],
                        "content": block.get("content", ""),
                    })
                elif block.get("type") == "text":
                    out.append({"role": "user", "content": block["text"]})

    return out


class OpenAIProvider(LLMProvider):
    """LLM provider backed by the OpenAI Chat Completions API."""

    def __init__(self, model: str = "gpt-4o", api_key: str | None = None) -> None:
        from openai import AsyncOpenAI

        self.model = model
        self._client = AsyncOpenAI(api_key=api_key)  # reads OPENAI_API_KEY if None

    async def complete(
        self,
        messages: list[Message],
        tools: list[mcp_types.Tool],
        system_prompt: str,
    ) -> LLMResponse:
        api_tools = [_mcp_tool_to_openai(t) for t in tools]
        api_messages = _messages_to_openai(messages, system_prompt)

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": api_messages,
        }
        if api_tools:
            kwargs["tools"] = api_tools

        log.debug(
            "OpenAI API request:\n%s",
            json.dumps(kwargs, indent=2, default=str),
        )

        response = await self._client.chat.completions.create(**kwargs)

        log.debug(
            "OpenAI API response:\n%s",
            json.dumps(response.model_dump(), indent=2, default=str),
        )

        choice = response.choices[0].message

        text = choice.content
        tool_calls: list[ToolCall] = []

        if choice.tool_calls:
            for tc in choice.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=json.loads(tc.function.arguments),
                    )
                )

        return LLMResponse(text=text, tool_calls=tool_calls)


# ---------------------------------------------------------------------------
# Google Gemini implementation
# ---------------------------------------------------------------------------


def _mcp_tool_to_google(tools: list[mcp_types.Tool]) -> Any:
    """Convert MCP Tools to a Google GenAI Tool with FunctionDeclarations."""
    from google.genai import types

    declarations = []
    for tool in tools:
        declarations.append(
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description or "",
                parameters_json_schema=tool.inputSchema,
            )
        )
    return types.Tool(function_declarations=declarations)


def _messages_to_google(messages: list[Message]) -> list[Any]:
    """Convert our generic message list into Google GenAI Content objects.

    Translates Anthropic-style content blocks into Gemini's Content/Part
    format with function_call and function_response parts.
    """
    from google.genai import types

    contents: list[types.Content] = []

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        # Google uses "model" instead of "assistant"
        gemini_role = "model" if role == "assistant" else "user"

        if isinstance(content, str):
            contents.append(types.Content(
                role=gemini_role,
                parts=[types.Part.from_text(text=content)],
            ))
            continue

        # content is a list of blocks
        parts: list[types.Part] = []
        for block in content:
            block_type = block.get("type")

            if block_type == "text":
                parts.append(types.Part.from_text(text=block["text"]))

            elif block_type == "tool_use":
                # Assistant requesting a function call
                parts.append(types.Part(
                    function_call=types.FunctionCall(
                        name=block["name"],
                        args=block["input"],
                    )
                ))

            elif block_type == "tool_result":
                # Tool result — sent as function_response
                result_content = block.get("content", "")
                # Try to parse as JSON dict, fall back to wrapping in a dict
                try:
                    response_dict = json.loads(result_content) if isinstance(result_content, str) else result_content
                    if not isinstance(response_dict, dict):
                        response_dict = {"result": response_dict}
                except (json.JSONDecodeError, TypeError):
                    response_dict = {"result": result_content}

                parts.append(types.Part.from_function_response(
                    name=block.get("_function_name", "unknown"),
                    response=response_dict,
                ))

        if parts:
            contents.append(types.Content(role=gemini_role, parts=parts))

    return contents


class GoogleProvider(LLMProvider):
    """LLM provider backed by Google's Gemini API."""

    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None) -> None:
        from google import genai
        from google.genai import types

        self.model = model
        self._types = types
        # Reads GOOGLE_API_KEY if api_key is None
        self._client = genai.Client(api_key=api_key)

    async def complete(
        self,
        messages: list[Message],
        tools: list[mcp_types.Tool],
        system_prompt: str,
    ) -> LLMResponse:
        types = self._types
        api_tool = _mcp_tool_to_google(tools) if tools else None
        api_contents = _messages_to_google(messages)

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        )
        if api_tool:
            config.tools = [api_tool]

        log.debug(
            "Google API request:\n  model=%s\n  system=%s\n  contents=%s\n  tools=%s",
            self.model, system_prompt[:200], repr(api_contents), repr(api_tool),
        )

        response = await self._client.aio.models.generate_content(
            model=self.model,
            contents=api_contents,
            config=config,
        )

        log.debug("Google API response:\n%s", response)

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        if response.candidates and response.candidates[0].content:
            for part in response.candidates[0].content.parts:
                if part.text:
                    text_parts.append(part.text)
                elif part.function_call:
                    # Google has no tool-call ID — synthesize one from the name
                    call_id = f"google_{part.function_call.name}_{len(tool_calls)}"
                    tool_calls.append(
                        ToolCall(
                            id=call_id,
                            name=part.function_call.name,
                            arguments=dict(part.function_call.args) if part.function_call.args else {},
                        )
                    )

        return LLMResponse(
            text="\n".join(text_parts) if text_parts else None,
            tool_calls=tool_calls,
        )
