"""Shared PID file utilities for managing Retreaver processes."""

from __future__ import annotations

import os
import signal
import sys
import time
from pathlib import Path

PID_DIR = Path.home() / ".retreaver"


def write_pid(name: str) -> None:
    """Write the current process PID to ~/.retreaver/<name>.pid."""
    PID_DIR.mkdir(parents=True, exist_ok=True)
    (PID_DIR / f"{name}.pid").write_text(str(os.getpid()))


def read_pid(name: str) -> int | None:
    """Read a PID from ~/.retreaver/<name>.pid, or None if missing."""
    pid_file = PID_DIR / f"{name}.pid"
    if not pid_file.exists():
        return None
    try:
        return int(pid_file.read_text().strip())
    except (ValueError, OSError):
        return None


def remove_pid(name: str) -> None:
    """Delete the PID file for *name* if it exists."""
    pid_file = PID_DIR / f"{name}.pid"
    pid_file.unlink(missing_ok=True)


def is_running(name: str) -> bool:
    """Return True if the process recorded in the PID file is alive."""
    pid = read_pid(name)
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        # Process exists but we don't own it — still "running".
        return True
    return True


def stop_process(name: str) -> None:
    """Send SIGTERM to the process and wait briefly for it to exit."""
    pid = read_pid(name)
    if pid is None:
        print(f"{name} is not running (no PID file).")
        return

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        print(f"{name} is not running (stale PID file, pid {pid}).")
        remove_pid(name)
        return
    except PermissionError:
        print(f"{name} (pid {pid}) is running but owned by another user.")
        return

    print(f"Stopping {name} (pid {pid}) ...")
    os.kill(pid, signal.SIGTERM)

    # Wait up to 5 seconds for the process to exit.
    for _ in range(50):
        time.sleep(0.1)
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            print(f"{name} stopped.")
            remove_pid(name)
            return

    print(f"{name} (pid {pid}) did not exit in time. You may need to kill it manually.")


def status_process(name: str) -> None:
    """Print whether the process is running and its PID."""
    pid = read_pid(name)
    if pid is None:
        print(f"{name} is not running (no PID file).")
        return

    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        print(f"{name} is not running (stale PID file, pid {pid}).")
        return
    except PermissionError:
        print(f"{name} is running (pid {pid}, owned by another user).")
        return

    print(f"{name} is running (pid {pid}).")


def handle_command(name: str) -> bool:
    """Check sys.argv for a stop/status subcommand.

    Returns True if a command was handled (caller should exit).
    Returns False if the process should start normally.
    """
    # Look for a bare "stop" or "status" anywhere in argv.  This keeps it
    # compatible with argparse — the caller's parser won't see these tokens
    # because we intercept before parsing.
    args = sys.argv[1:]
    if "stop" in args:
        stop_process(name)
        return True
    if "status" in args:
        status_process(name)
        return True
    return False
