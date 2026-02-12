#!/usr/bin/env python
"""Commit-msg hook: enforce commit message standard for code commits.

Rules:
- If code/config files are staged, at least one .md must be staged (twin-commit).
- For such commits, the commit message must:
  - follow Conventional Commits-ish prefix: type(scope)?: subject
  - include the literal suffix: "| docs updated"
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


DOC_EXTENSIONS = {".md"}
CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".kdl",
    ".sql",
    ".sh",
    ".ps1",
    ".bat",
    ".cmd",
    ".env",
}
CODE_FILENAMES = {"dockerfile", ".pre-commit-config.yaml", ".pre-commit-config.yml"}

TYPE_RE = re.compile(
    r"^(feat|fix|refactor|chore|docs|test|perf|build|ci|style|revert)"
    r"(\([a-z0-9._-]+\))?:\s+.+",
)


def _run_git(args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git command failed")
    return completed.stdout


def _get_staged_files() -> list[str]:
    output = _run_git(["diff", "--cached", "--name-only"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def _is_doc(path_str: str) -> bool:
    return Path(path_str).suffix.lower() in DOC_EXTENSIONS


def _is_code_or_config(path_str: str) -> bool:
    path = Path(path_str)
    if path.suffix.lower() in DOC_EXTENSIONS:
        return False
    if path.suffix.lower() in CODE_EXTENSIONS:
        return True
    if path.name.lower() in CODE_FILENAMES:
        return True
    return False


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("[commit-msg] Missing commit message file path")
        return 1

    msg_file = Path(argv[1])
    try:
        first_line = msg_file.read_text(encoding="utf-8").strip().splitlines()[0]
        message = first_line.strip()
    except Exception as exc:
        print(f"[commit-msg] Unable to read commit message: {exc}")
        return 1

    try:
        staged_files = _get_staged_files()
    except Exception as exc:
        print(f"[commit-msg] Unable to read staged files: {exc}")
        return 1

    has_docs = any(_is_doc(f) for f in staged_files)
    has_code = any(_is_code_or_config(f) for f in staged_files)

    if not has_code:
        return 0

    if not has_docs:
        print("[commit-msg] Blocked: code/config commits must include .md updates (twin-commit).")
        return 1

    if not TYPE_RE.match(message):
        print("[commit-msg] Blocked: commit message must follow: type(scope)?: subject")
        print("[commit-msg] Examples:")
        print("  feat(api): add lyrics ingest endpoint | docs updated")
        print("  fix(worker): handle supabase timeout | docs updated")
        return 1

    if "| docs updated" not in message:
        print("[commit-msg] Blocked: code commits must include the suffix: '| docs updated'")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
