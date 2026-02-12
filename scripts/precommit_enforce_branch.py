#!/usr/bin/env python
"""Pre-commit hook: enforce feature-branch discipline.

Blocks committing code/config directly on protected baseline branches.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


PROTECTED_BRANCHES = {"main", "master", "v2.1"}

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


def _get_branch() -> str:
    return _run_git(["rev-parse", "--abbrev-ref", "HEAD"]).strip()


def _get_staged_files() -> list[str]:
    output = _run_git(["diff", "--cached", "--name-only"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def _is_code_or_config(path_str: str) -> bool:
    path = Path(path_str)
    if path.suffix.lower() in DOC_EXTENSIONS:
        return False
    if path.suffix.lower() in CODE_EXTENSIONS:
        return True
    if path.name.lower() in CODE_FILENAMES:
        return True
    return False


def main() -> int:
    try:
        branch = _get_branch()
        staged_files = _get_staged_files()
    except Exception as exc:  # pragma: no cover
        print(f"[branch-guard] Unable to validate branch: {exc}")
        return 1

    if branch == "HEAD":
        return 0

    if branch.lower() not in PROTECTED_BRANCHES:
        return 0

    has_code = any(_is_code_or_config(f) for f in staged_files)
    if not has_code:
        return 0

    print(f"[branch-guard] Blocked: do not commit code directly on '{branch}'.")
    print("[branch-guard] Create a feature branch from v2.1:")
    print("  git checkout v2.1")
    print("  git pull")
    print("  git checkout -b feature/brief-description")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
