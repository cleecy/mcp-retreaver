# Retreaver MCP


The project has four components:

- **Read server** — MCP server exposing read-only Retreaver API endpoints (campaigns, targets, calls, etc.)
- **Write server** — MCP server exposing write endpoints (create, update, delete)
- **Host** — An MCP client/orchestrator that connects to both servers, talks to an LLM, and exposes a WebSocket interface for chat
- **Telegram bot** — Bridges Telegram messages to the host's WebSocket, so you can chat with the assistant from Telegram

## Project Structure

```
src/
  retreaver_mcp_servers/
    client.py          # Shared async HTTP client for the Retreaver API
    process.py         # PID file utilities (start/stop/status)
    launcher.py        # Single-command launcher for all services
    read_server.py     # MCP server — GET endpoints
    write_server.py    # MCP server — POST/PUT/DELETE endpoints
  retreaver_host/
    model_interface.py # LLM provider abstraction (Anthropic, OpenAI, Google)
    orchestrator.py    # Agentic tool-use chat loop
    ws_server.py       # WebSocket server for chat integration
    main.py            # Entry point — wires everything together
  retreaver_telegram/
    bot.py             # Telegram ↔ WebSocket bridge
    main.py            # Entry point
```

## Prerequisites

- Python 3.10+
- A Retreaver account (API key + company ID)
- An API key for at least one LLM provider (Anthropic, OpenAI, or Google)

## Installation

```bash
git clone <repo-url>
cd mcp-retreaver
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Configuration

All configuration is done through environment variables. You can set them inline, export them, or put them in a `.env` file in the project root (loaded automatically via `python-dotenv`).

### Required

| Variable | Description |
|---|---|
| `RETREAVER_API_KEY` | Your Retreaver API key |
| `RETREAVER_COMPANY_ID` | Your Retreaver company ID |

Plus one of the following, depending on which LLM provider you use:

| Variable | Provider |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic (default) |
| `OPENAI_API_KEY` | OpenAI |
| `GOOGLE_API_KEY` | Google Gemini |

### Optional

| Variable | Default | Description |
|---|---|---|
| `RETREAVER_BASE_URL` | `https://api.retreaver.com` | Retreaver API base URL |
| `LLM_PROVIDER` | `anthropic` | LLM provider: `anthropic`, `openai`, or `google` |
| `LLM_MODEL` | *(per provider)* | Override the default model |
| `MCP_READ_SERVER_URL` | `http://localhost:8001/sse` | Read server SSE endpoint |
| `MCP_WRITE_SERVER_URL` | `http://localhost:8002/sse` | Write server SSE endpoint |
| `WS_HOST` | `0.0.0.0` | WebSocket server bind address |
| `WS_PORT` | `8080` | WebSocket server port |
| `TELEGRAM_BOT_TOKEN` | *(required for bot)* | Telegram bot token from @BotFather |
| `TELEGRAM_ALLOWED_USERS` | *(empty = all)* | Comma-separated allowlist of Telegram user IDs and/or @usernames |
| `WS_URL` | `ws://localhost:8080` | WebSocket endpoint the Telegram bot connects to |

### Example `.env` file

```
RETREAVER_API_KEY=your-retreaver-api-key
RETREAVER_COMPANY_ID=your-company-id
ANTHROPIC_API_KEY=your-anthropic-api-key
```

## Running

### Quick start (recommended)

```bash
retreaver
```

This launches the read server, write server, and host together in one command. Use `retreaver stop` to shut everything down and `retreaver status` to check.

### Manual start

Alternatively, start each process in a separate terminal. The sequence matters.

#### 1. Start the read server

```bash
retreaver-read
```

Listens on port 8001 by default. Override with `--port` and `--host`.

#### 2. Start the write server

```bash
retreaver-write
```

Listens on port 8002 by default.

#### 3. Start the host

```bash
retreaver-host
```

This connects to both MCP servers, initializes the LLM provider, and starts the WebSocket server on port 8080.

### 4. Start the Telegram bot (optional)

1. Message [@BotFather](https://t.me/BotFather) on Telegram and create a new bot to get a token.
2. Add the token to your `.env`:
   ```
   TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
   ```
3. Start the bot:
   ```bash
   retreaver-telegram
   ```

The bot connects to the host's WebSocket (`ws://localhost:8080` by default). Each Telegram chat gets its own WebSocket connection, so conversations are independent.

### Managing Processes

Each command supports `stop` and `status` subcommands. PID files are stored in `~/.retreaver/`.

```bash
# Check if a process is running
retreaver-read status
retreaver-write status
retreaver-host status
retreaver-telegram status

# Stop a running process
retreaver-read stop
retreaver-write stop
retreaver-host stop
retreaver-telegram stop
```

The `start` subcommand is the default and can be omitted — `retreaver-read` and `retreaver-read start` are equivalent. All existing flags (like `--port` and `--host`) continue to work as before.

You should see output like:

```
INFO retreaver_host.main: Using LLM provider: anthropic (model=claude-sonnet-4-20250514)
INFO retreaver_host.main: Connecting to read server at http://localhost:8001/sse ...
INFO retreaver_host.main: Connecting to write server at http://localhost:8002/sse ...
INFO retreaver_host.main: Connected — 75 tools available: get_calls, get_call, ...
INFO retreaver_host.ws_server: WebSocket server listening on ws://0.0.0.0:8080
```

## Chatting with the assistant

Connect any WebSocket client to `ws://localhost:8080`. Messages use a simple JSON protocol:

```
-> {"text": "your message"}
<- {"text": "assistant reply"}
<- {"error": "error description"}   (on failure)
```

Each WebSocket connection gets its own conversation with independent message history.

### Using websocat

```bash
brew install websocat   # if not installed
websocat ws://localhost:8080
```

Then type JSON messages:

```json
{"text": "list my campaigns"}
{"text": "how many targets do I have?"}
{"text": "create a new campaign with cid test123"}
```

### Using Python

```python
import asyncio, json, websockets

async def chat():
    async with websockets.connect("ws://localhost:8080") as ws:
        await ws.send(json.dumps({"text": "list my campaigns"}))
        response = json.loads(await ws.recv())
        print(response["text"])

asyncio.run(chat())
```

## LLM Providers

| `LLM_PROVIDER` | Default Model | API Key Variable |
|---|---|---|
| `anthropic` | `claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY` |
| `openai` | `gpt-4o` | `OPENAI_API_KEY` |
| `google` | `gemini-2.5-flash` | `GOOGLE_API_KEY` |

Override the default model with `LLM_MODEL`:



```bash
LLM_PROVIDER=openai LLM_MODEL=gpt-4o-mini retreaver-host
```

## Architecture

```
                WebSocket clients
                     |
                 ws_server.py
                     |
                orchestrator.py  <-- agentic tool-use loop
                   /    \
        model_interface.py    ClientSessionGroup
             (LLM API)    /          \
                   read_server    write_server
                       \            /
                     Retreaver API
```

The orchestrator runs a loop for each user message:

1. Send the conversation + available tools to the LLM
2. If the LLM returns tool calls, execute them via MCP
3. Feed the results back to the LLM
4. Repeat until the LLM responds with plain text (max 15 rounds)

Tool routing is automatic — the `ClientSessionGroup` aggregates tools from both servers and dispatches `call_tool()` to whichever server owns the tool.


