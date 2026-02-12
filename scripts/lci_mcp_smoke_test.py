#!/usr/bin/env python3
"""LCI/MCP smoke test for local stability.

Runs the standard LCI checks and then attempts to start the MCP bridge briefly.

Usage:
  python scripts/lci_mcp_smoke_test.py
  python scripts/lci_mcp_smoke_test.py --query "guardian_loop" --timeout 4

Exit codes:
  0: success
  1: failure
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from shutil import which


def _npx_prefix() -> list[str]:
    """Return a prefix that can execute npx reliably.

    On Windows, npx is commonly a .cmd shim which cannot be executed directly
    via CreateProcess without going through cmd.exe.
    """

    npx_path = which("npx") or which("npx.cmd") or "npx"
    if os.name != "nt":
        return [npx_path]

    lower = npx_path.lower()
    if lower.endswith((".cmd", ".bat")):
        return ["cmd.exe", "/c", npx_path]

    return [npx_path]


def _run(cmd: list[str], timeout_s: float | None = None) -> int:
    printable = " ".join(cmd)
    print(f"[lci-smoke] $ {printable}")
    try:
        completed = subprocess.run(cmd, check=False, timeout=timeout_s)
    except subprocess.TimeoutExpired:
        print(f"[lci-smoke] TIMEOUT after {timeout_s}s: {printable}")
        return 124
    if completed.returncode != 0:
        print(f"[lci-smoke] FAILED ({completed.returncode}): {' '.join(cmd)}")
    return completed.returncode


def _run_capture(cmd: list[str], timeout_s: float | None = None) -> tuple[int, str]:
    printable = " ".join(cmd)
    print(f"[lci-smoke] $ {printable}")
    try:
        completed = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        print(f"[lci-smoke] TIMEOUT after {timeout_s}s: {printable}")
        return 124, ""
    output = (completed.stdout or "").strip()
    if completed.returncode != 0:
        print(f"[lci-smoke] FAILED ({completed.returncode}): {' '.join(cmd)}")
        if output:
            print(output)
    return completed.returncode, output


def _wait_for_ready(prefix: list[str], wait_s: float) -> bool:
    start = time.time()
    while time.time() - start < wait_s:
        rc, out = _run_capture([*prefix, "lci", "status", "--verbose"], timeout_s=20)
        if rc == 0 and "Status: Ready" in out:
            return True
        time.sleep(1.0)
    return False


def _start_mcp(timeout_s: float) -> int:
    cmd = [*_npx_prefix(), "lci", "mcp"]
    print(f"[lci-smoke] $ {' '.join(cmd)} (running for {timeout_s}s)")

    creationflags = 0
    if os.name == "nt" and hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP"):
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        creationflags=creationflags,
    )

    try:
        start = time.time()
        while time.time() - start < timeout_s:
            if proc.poll() is not None:
                rc = proc.returncode
                print(f"[lci-smoke] FAILED: MCP bridge exited early with code {rc}")
                if proc.stdout is not None:
                    try:
                        remaining = proc.stdout.read()
                    except Exception:
                        remaining = ""
                    remaining = (remaining or "").strip()
                    if remaining:
                        print("[lci-smoke] MCP output (partial):")
                        for line in remaining.splitlines()[:50]:
                            print(f"  {line}")
                return 1
            time.sleep(0.1)

        print(f"[lci-smoke] SUCCESS: MCP bridge stayed alive for {timeout_s}s")
        return 0
    finally:
        if proc.poll() is None:
            try:
                print("[lci-smoke] Stopping MCP bridge...")
                proc.terminate()
            except Exception:
                pass
            try:
                proc.wait(timeout=2)
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="guardian_loop")
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--wait", type=float, default=60.0)
    parser.add_argument("--no-start-server", action="store_true")
    parser.add_argument(
        "--skip-list",
        action="store_true",
        help="Skip `lci list` step (useful on some Windows shells where list output may block)",
    )
    args = parser.parse_args(argv)

    prefix = _npx_prefix()
    try:
        # Note: `lci status` auto-starts the server in the background when needed.
        # Avoid calling `lci server --daemon` directly here because it may not detach
        # consistently across environments.
        if not args.no_start_server:
            _run([*prefix, "lci", "status", "--verbose"], timeout_s=30)

        if not _wait_for_ready(prefix, args.wait):
            print(
                f"[lci-smoke] FAILED: LCI server did not become ready within {args.wait}s"
            )
            return 1

        if not args.skip_list:
            rc, list_out = _run_capture([*prefix, "lci", "list"], timeout_s=30)
            if rc != 0:
                return 1

            total_ok = "Total:" in list_out and "files would be indexed" in list_out
            if not total_ok:
                print(
                    "[lci-smoke] WARNING: Unable to parse 'Total: ... files would be indexed' from lci list output"
                )

            # Only fail if the actual `.git/` directory appears, not `.github/...`.
            first_lines = list_out.splitlines()[:50]
            if any(
                line == ".git" or line.startswith(".git/") or "/.git/" in line
                for line in first_lines
            ):
                print(
                    "[lci-smoke] FAILED: .git appears in first 50 listed files; exclude patterns likely not applied"
                )
                return 1

        if _run([*prefix, "lci", "search", args.query], timeout_s=30) != 0:
            return 1

        if _start_mcp(args.timeout) != 0:
            return 1

        print("[lci-smoke] OK")
        return 0
    finally:
        _run([*prefix, "lci", "shutdown"], timeout_s=30)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
