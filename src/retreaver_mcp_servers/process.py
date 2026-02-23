"""Shared PID file utilities for managing Retreaver processes."""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

_WIN = sys.platform == "win32"

PID_DIR = Path.home() / ".retreaver"


def _pid_exists(pid: int) -> bool:
    """Check if a process with the given PID is alive."""
    if _WIN:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x100000, False, pid)  # SYNCHRONIZE
        if handle:
            kernel32.CloseHandle(handle)
            return True
        return False
    else:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True


def _terminate(pid: int) -> None:
    """Send a termination signal to a process."""
    if _WIN:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(1, False, pid)  # PROCESS_TERMINATE
        if handle:
            kernel32.TerminateProcess(handle, 1)
            kernel32.CloseHandle(handle)
    else:
        import signal
        os.kill(pid, signal.SIGTERM)


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
    return _pid_exists(pid)


def stop_process(name: str) -> None:
    """Terminate the process and wait briefly for it to exit."""
    pid = read_pid(name)
    if pid is None:
        print(f"{name} is not running (no PID file).")
        return

    if not _pid_exists(pid):
        print(f"{name} is not running (stale PID file, pid {pid}).")
        remove_pid(name)
        return

    print(f"Stopping {name} (pid {pid}) ...")
    _terminate(pid)

    # Wait up to 5 seconds for the process to exit.
    for _ in range(50):
        time.sleep(0.1)
        if not _pid_exists(pid):
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

    if _pid_exists(pid):
        print(f"{name} is running (pid {pid}).")
    else:
        print(f"{name} is not running (stale PID file, pid {pid}).")


def handle_command(name: str) -> bool:
    """Check sys.argv for a stop/status subcommand.

    Returns True if a command was handled (caller should exit).
    Returns False if the process should start normally.
    """
    args = sys.argv[1:]
    if "stop" in args:
        stop_process(name)
        return True
    if "status" in args:
        status_process(name)
        return True
    return False
