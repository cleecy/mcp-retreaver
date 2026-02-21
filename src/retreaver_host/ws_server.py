"""Minimal WebSocket server for chat integration.

Accepts either plain text or JSON:
  -> "user message"              (plain text)
  -> {"text": "user message"}    (JSON)
  <- {"text": "assistant reply"}
  <- {"error": "description"}
"""

from __future__ import annotations

import json
import logging
from typing import Any

import websockets
from mcp import ClientSessionGroup

from .model_interface import LLMProvider
from .orchestrator import Conversation, run_turn

log = logging.getLogger(__name__)


async def _handle_connection(
    ws: Any,
    llm: LLMProvider,
    mcp_group: ClientSessionGroup,
) -> None:
    """Handle a single WebSocket connection with its own conversation state."""
    conversation = Conversation()
    log.info("New WebSocket connection from %s", ws.remote_address)

    async for raw in ws:
        try:
            # Accept both plain text and JSON {"text": "..."}
            try:
                msg = json.loads(raw)
                user_text = msg.get("text", "").strip()
            except (json.JSONDecodeError, AttributeError):
                user_text = raw.strip() if isinstance(raw, str) else raw.decode().strip()

            if not user_text:
                await ws.send(json.dumps({"error": "Empty message"}))
                continue

            log.info("User: %s", user_text[:120])
            reply = await run_turn(user_text, conversation, llm, mcp_group)
            await ws.send(json.dumps({"text": reply}))

        except Exception as exc:
            log.exception("Error processing message")
            await ws.send(json.dumps({"error": str(exc)}))


async def start_ws_server(
    llm: LLMProvider,
    mcp_group: ClientSessionGroup,
    host: str = "0.0.0.0",
    port: int = 8080,
) -> Any:
    """Start the WebSocket server and return the server object."""

    async def handler(ws: Any) -> None:
        await _handle_connection(ws, llm, mcp_group)

    server = await websockets.serve(handler, host, port)
    log.info("WebSocket server listening on ws://%s:%d", host, port)
    return server
