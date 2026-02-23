"""Telegram bot that bridges messages to the Retreaver host WebSocket."""

from __future__ import annotations

import json
import logging

import websockets
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

log = logging.getLogger(__name__)


async def _handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Forward a Telegram message to the WebSocket and relay the reply."""
    if update.message is None or update.message.text is None:
        return

    # Check allowlist (user IDs and/or usernames)
    allowed_ids: set = context.bot_data.get("allowed_user_ids", set())
    allowed_names: set = context.bot_data.get("allowed_usernames", set())
    if (allowed_ids or allowed_names) and update.effective_user:
        user = update.effective_user
        id_ok = user.id in allowed_ids if allowed_ids else False
        name_ok = (user.username or "").lower() in allowed_names if allowed_names else False
        if not id_ok and not name_ok:
            log.warning("Unauthorized user %s (%s)", user.id, user.username)
            await update.message.reply_text("You are not authorized to use this bot.")
            return

    ws_url: str = context.bot_data["ws_url"]
    chat_id = update.effective_chat.id  # type: ignore[union-attr]
    user_text = update.message.text.strip()

    if not user_text:
        return

    # Maintain one persistent WebSocket per chat for conversation continuity.
    ws_connections: dict = context.bot_data.setdefault("ws_connections", {})

    ws = ws_connections.get(chat_id)

    # Open a new connection if we don't have one or it's closed.
    if ws is None or ws.close_code is not None:
        try:
            ws = await websockets.connect(ws_url)
            ws_connections[chat_id] = ws
            log.info("Opened WebSocket for chat %s", chat_id)
        except Exception:
            log.exception("Failed to connect to WebSocket at %s", ws_url)
            await update.message.reply_text("Could not reach the Retreaver host. Is it running?")
            return

    try:
        await ws.send(json.dumps({"text": user_text}))
        raw_reply = await ws.recv()
        reply = json.loads(raw_reply)

        if "error" in reply:
            await update.message.reply_text(f"Error: {reply['error']}")
        else:
            await update.message.reply_text(reply.get("text", "(empty reply)"))

    except websockets.exceptions.ConnectionClosed:
        log.warning("WebSocket closed for chat %s, removing", chat_id)
        ws_connections.pop(chat_id, None)
        await update.message.reply_text("Connection lost. Please send your message again.")
    except Exception:
        log.exception("Error relaying message for chat %s", chat_id)
        ws_connections.pop(chat_id, None)
        await update.message.reply_text("Something went wrong. Please try again.")


def build_app(token: str, ws_url: str, allowed_user_ids: set[int] | None = None, allowed_usernames: set[str] | None = None):
    """Build and return a configured Telegram Application (not yet running)."""
    app = ApplicationBuilder().token(token).build()
    app.bot_data["ws_url"] = ws_url
    app.bot_data["allowed_user_ids"] = allowed_user_ids or set()
    app.bot_data["allowed_usernames"] = allowed_usernames or set()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_message))
    return app
