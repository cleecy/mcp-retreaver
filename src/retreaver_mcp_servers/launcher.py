"""Single-command launcher for all Retreaver services."""

from __future__ import annotations

import signal
import subprocess
import sys
import time

from .process import is_running, stop_process

_SERVICES = [
    ("retreaver-read", ["retreaver-read"]),
    ("retreaver-write", ["retreaver-write"]),
    ("retreaver-host", ["retreaver-host"]),
]


def _stop_all() -> None:
    for name, _ in reversed(_SERVICES):
        if is_running(name):
            stop_process(name)


def _status_all() -> None:
    from .process import status_process

    for name, _ in _SERVICES:
        status_process(name)


def main() -> None:
    args = sys.argv[1:]

    if "stop" in args:
        _stop_all()
        return

    if "status" in args:
        _status_all()
        return

    # Start each service as a subprocess.
    procs: list[tuple[str, subprocess.Popen]] = []

    def shutdown(signum=None, frame=None) -> None:
        print("\nShutting down all services...")
        for name, proc in reversed(procs):
            if proc.poll() is None:
                print(f"  Stopping {name} (pid {proc.pid})...")
                proc.terminate()
        # Wait for all to exit.
        for name, proc in procs:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"  Force-killing {name} (pid {proc.pid})")
                proc.kill()
        print("All services stopped.")

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print("Starting Retreaver services...")

    for name, cmd in _SERVICES:
        print(f"  Starting {name}...")
        proc = subprocess.Popen(cmd)
        procs.append((name, proc))
        # Give MCP servers a moment to bind their ports before the host connects.
        if name in ("retreaver-read", "retreaver-write"):
            time.sleep(1)

    print(f"\nAll services running. Press Ctrl+C to stop.\n")
    print(f"  Read server:  http://localhost:8001/sse")
    print(f"  Write server: http://localhost:8002/sse")
    print(f"  WebSocket:    ws://localhost:8080")
    print()

    # Wait for any subprocess to exit unexpectedly.
    try:
        while True:
            for name, proc in procs:
                ret = proc.poll()
                if ret is not None:
                    print(f"\n{name} exited with code {ret}. Shutting down...")
                    shutdown()
                    sys.exit(ret)
            time.sleep(0.5)
    except SystemExit:
        raise
    except Exception:
        shutdown()


if __name__ == "__main__":
    main()
