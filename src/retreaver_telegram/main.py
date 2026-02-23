"""Entry point for the Retreaver Telegram bot."""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

_NAME = "retreaver-telegram"


def main() -> None:
    from retreaver_mcp_servers.process import handle_command, write_pid

    if handle_command(_NAME):
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log = logging.getLogger(__name__)

    load_dotenv()

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set. Get one from @BotFather on Telegram.")

    ws_url = os.environ.get("WS_URL", "ws://localhost:8080")

    allowed_raw = os.environ.get("TELEGRAM_ALLOWED_USERS", "")
    allowed_user_ids: set[int] = set()
    allowed_usernames: set[str] = set()
    for entry in allowed_raw.split(","):
        entry = entry.strip()
        if not entry:
            continue
        if entry.startswith("@"):
            allowed_usernames.add(entry.lstrip("@").lower())
        else:
            allowed_user_ids.add(int(entry))

    write_pid(_NAME)
    log.info("Starting Telegram bot (ws_url=%s, allowed_ids=%s, allowed_usernames=%s) ...", ws_url, allowed_user_ids or "all", allowed_usernames or "all")

    from .bot import build_app

    app = build_app(token, ws_url, allowed_user_ids, allowed_usernames)
    app.run_polling()

    from retreaver_mcp_servers.process import remove_pid

    remove_pid(_NAME)


if __name__ == "__main__":
    main()
