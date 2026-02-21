"""Entry point for the Retreaver MCP host.

Reads configuration from environment variables, connects to both MCP servers
via a ClientSessionGroup, and starts the WebSocket server.
"""
#comments are my own (cyle), not ai generated. I added them for myself. disregard if you possess a higher intelligence than cyle

from __future__ import annotations

import asyncio
import logging
import os
import signal

from dotenv import load_dotenv
from mcp import ClientSessionGroup
from mcp.client.session_group import SseServerParameters

from .model_interface import AnthropicProvider, GoogleProvider, LLMProvider, OpenAIProvider
from .ws_server import start_ws_server

log = logging.getLogger(__name__)

#used in main()
_NAME = "retreaver-host"

#runs the main logic of the host process. spins up the mcp clients, mcp servers, starts the websocket server, and runs the chat loop.
async def _run() -> None:
    from retreaver_mcp_servers.process import remove_pid, write_pid
#pulls config variables from .env into os.environ
    load_dotenv()

    #writes the pid to a file so it can be killed easily with terminal commands
    write_pid(_NAME)

#reads variables from os.environ into python variables for runtime. some are not liekly to change
    read_url = os.environ.get("MCP_READ_SERVER_URL", "http://localhost:8001/sse")
    write_url = os.environ.get("MCP_WRITE_SERVER_URL", "http://localhost:8002/sse")
    ws_host = os.environ.get("WS_HOST", "0.0.0.0")
    ws_port = int(os.environ.get("WS_PORT", "8080"))
    llm_provider = os.environ.get("LLM_PROVIDER", "anthropic").lower()
    llm_model = os.environ.get("LLM_MODEL", "")
#maps the .env config string to the python class and default model. note, this is where default models are hardcoded. classes imported from model_interface.py
    PROVIDER_DEFAULTS = {
        "anthropic": (AnthropicProvider, "claude-sonnet-4-20250514"),
        "openai": (OpenAIProvider, "gpt-4o"),
        "google": (GoogleProvider, "gemini-2.5-flash"),
    }
#if the .env config string is not in the PROVIDER_DEFAULTS dict, error out.
    if llm_provider not in PROVIDER_DEFAULTS:
        raise SystemExit(f"Unknown LLM_PROVIDER={llm_provider!r}. Choose from: {', '.join(PROVIDER_DEFAULTS)}")
#if the .env config string is in the PROVIDER_DEFAULTS dict, get the python class and default model.
    provider_cls, default_model = PROVIDER_DEFAULTS[llm_provider]
    
    llm = provider_cls(model=llm_model or default_model)
    #nice to see what we're using
    log.info("Using LLM provider: %s (model=%s)", llm_provider, llm_model or default_model)

#mcp standards are 1 client : 1 server. this class makes it easy to spin up and manage multiple clients and their connections. json-rpc data. stdio transport
    async with ClientSessionGroup() as mcp_server_group:
        log.info("Connecting to read server at %s ...", read_url)
        await mcp_server_group.connect_to_server(SseServerParameters(url=read_url))

        log.info("Connecting to write server at %s ...", write_url)
        await mcp_server_group.connect_to_server(SseServerParameters(url=write_url))

        tool_names = list(mcp_server_group.tools.keys())
        log.info("Connected — %d tools available: %s", len(tool_names), ", ".join(tool_names))

        ws_server = await start_ws_server(llm, mcp_server_group, ws_host, ws_port)

        #stops at the await stop.wait() line, until kill signals are sent. python event loop is listening, sets stop=True
        stop = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop.set)

        await stop.wait()
        log.info("Shutting down ...")
        ws_server.close()
        await ws_server.wait_closed()
        remove_pid(_NAME)

#right after entry
def main() -> None:
    from retreaver_mcp_servers.process import handle_command
#seems redundant, who would start the process and immediately check for a stop command?
    if handle_command(_NAME):
        return

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    asyncio.run(_run())

#entry
if __name__ == "__main__":
    main()
