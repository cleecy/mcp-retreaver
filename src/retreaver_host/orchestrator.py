"""Agentic chat-loop orchestrator.

Manages a conversation, sends messages to the LLM, executes tool calls via
the MCP ClientSessionGroup, and feeds results back until the LLM produces a
final text response.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mcp import ClientSessionGroup

from .model_interface import LLMProvider, LLMResponse, Message

log = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 15

_BASE_SYSTEM_PROMPT = """\
You are the Retreaver Assistant — an AI agent that helps users manage their \
Retreaver call-tracking account.

You have access to tools that can read and write Retreaver resources such as \
campaigns, targets, affiliates, numbers, number pools, contacts, caller lists, \
target groups, and more.

Your Identity:
- Be concise and helpful.
- When listing resources, summarise key fields rather than dumping raw JSON.
- Always confirm before performing destructive operations (delete).
- If a tool call fails, explain the error clearly and suggest a fix.
"""

_CONTEXT_GUIDE_PATH = Path(__file__).resolve().parent.parent.parent / "retreaver_agent_context_guide.md"


def _load_system_prompt() -> str:
    """Build the full system prompt, appending the context guide if it exists and is non-empty."""
    prompt = _BASE_SYSTEM_PROMPT
    try:
        guide = _CONTEXT_GUIDE_PATH.read_text().strip()
        if guide:
            prompt += "\n" + guide + "\n"
    except FileNotFoundError:
        pass
    return prompt


SYSTEM_PROMPT = _load_system_prompt()


# ---------------------------------------------------------------------------
# Conversation state
# ---------------------------------------------------------------------------


@dataclass
class Conversation:
    """Holds the ordered list of messages for a single chat session."""

    messages: list[Message] = field(default_factory=list)

    def add_user_message(self, text: str) -> None:
        self.messages.append({"role": "user", "content": text})

    def add_assistant_message(self, response: LLMResponse) -> None:
        """Append the full assistant response (text + tool_use blocks)."""
        content: list[dict[str, Any]] = []
        if response.text:
            content.append({"type": "text", "text": response.text})
        for tc in response.tool_calls:
            content.append({
                "type": "tool_use",
                "id": tc.id,
                "name": tc.name,
                "input": tc.arguments,
            })
        self.messages.append({"role": "assistant", "content": content})

    def add_tool_results(self, results: list[dict[str, Any]]) -> None:
        """Append tool_result blocks as a single user message."""
        self.messages.append({"role": "user", "content": results})


# ---------------------------------------------------------------------------
# Turn runner
# ---------------------------------------------------------------------------


async def run_turn(
    user_text: str,
    conversation: Conversation,
    llm: LLMProvider,
    mcp_group: ClientSessionGroup,
) -> str:
    """Execute one full user turn, including any tool-use rounds.

    Returns the final assistant text reply.
    """
    conversation.add_user_message(user_text)

    tools = list(mcp_group.tools.values())

    for round_num in range(MAX_TOOL_ROUNDS):
        response = await llm.complete(conversation.messages, tools, SYSTEM_PROMPT)

        if not response.tool_calls:
            # No tool calls — we have a final text answer.
            text = response.text or ""
            if response.text:
                conversation.add_assistant_message(response)
            return text

        # Record the assistant turn that includes tool_use blocks.
        conversation.add_assistant_message(response)

        # Execute each tool call via MCP.
        tool_results: list[dict[str, Any]] = []
        for tc in response.tool_calls:
            log.info("Tool call [round %d]: %s(%s)", round_num + 1, tc.name, json.dumps(tc.arguments))
            try:
                result = await mcp_group.call_tool(tc.name, tc.arguments)
                # Serialize content blocks to a string for the LLM.
                parts = []
                for block in result.content:
                    if hasattr(block, "text"):
                        parts.append(block.text)
                    else:
                        parts.append(json.dumps(block.model_dump(), default=str))
                content = "\n".join(parts) if parts else "(no output)"
                is_error = result.isError
            except Exception as exc:
                log.exception("Tool call %s failed", tc.name)
                content = f"Error: {exc}"
                is_error = True

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tc.id,
                "content": content,
                "is_error": is_error,
                "_function_name": tc.name,  # Used by Google provider for matching
            })

        conversation.add_tool_results(tool_results)

    # Safety limit reached.
    return "I'm sorry, I reached the maximum number of tool rounds for this turn. Please try a simpler request."
