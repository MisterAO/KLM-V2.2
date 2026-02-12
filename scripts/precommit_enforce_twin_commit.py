#!/usr/bin/env python
"""Pre-commit hook: enforce the "twin-commit" rule.

If any code/config files are staged, at least one Markdown doc must also be staged.

Docs-only commits are allowed.
"""

from __future__ import annotations

import subprocess
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
CODE_FILENAMES = {
    "dockerfile",
    ".pre-commit-config.yaml",
    ".pre-commit-config.yml",
}


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
    suffix = path.suffix.lower()
    if suffix in DOC_EXTENSIONS:
        return False
    if suffix in CODE_EXTENSIONS:
        return True
    if path.name.lower() in CODE_FILENAMES:
        return True
    return False


def main() -> int:
    try:
        staged_files = _get_staged_files()
    except Exception as exc:  # pragma: no cover
        print(f"[twin-commit] Unable to read staged files: {exc}")
        return 1

    if not staged_files:
        return 0

    has_docs = any(_is_doc(f) for f in staged_files)
    has_code = any(_is_code_or_config(f) for f in staged_files)

    if has_code and not has_docs:
        print("[twin-commit] Blocked: code/config changes require at least one .md update.")
        print("[twin-commit] Add/update a relevant doc (README/SOP/session log) in this commit.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
