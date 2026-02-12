from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
from typing import Iterable


def _repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def _run(cmd: list[str], *, cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
    )


def _git_ls_files(cwd: pathlib.Path) -> list[pathlib.Path]:
    proc = _run(["git", "ls-files", "-z"], cwd=cwd)
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-files failed: {proc.stderr.strip()}")
    paths: list[pathlib.Path] = []
    for raw in proc.stdout.split("\0"):
        if not raw:
            continue
        paths.append(cwd / raw)
    return paths


def _is_probably_text(path: pathlib.Path) -> bool:
    suffix = path.suffix.lower()
    if suffix in {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".pdf",
        ".zip",
        ".7z",
        ".tar",
        ".gz",
        ".mp3",
        ".mp4",
    }:
        return False
    return True


def _iter_lines(path: pathlib.Path) -> Iterable[str]:
    with path.open("rb") as f:
        blob = f.read()
    try:
        text = blob.decode("utf-8")
    except UnicodeDecodeError:
        text = blob.decode("utf-8", errors="ignore")
    return text.splitlines()


def audit_no_committed_secrets(repo: pathlib.Path) -> list[str]:
    findings: list[str] = []
    patterns: list[tuple[str, re.Pattern[str]]] = [
        ("openrouter_key", re.compile(r"sk-or-[A-Za-z0-9_-]{16,}")),
        ("github_pat", re.compile(r"ghp_[A-Za-z0-9]{20,}")),
        ("aws_access_key", re.compile(r"AKIA[0-9A-Z]{16}")),
        (
            "private_key_block",
            re.compile(r"-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----"),
        ),
    ]
    for path in _git_ls_files(repo):
        if not path.exists() or not _is_probably_text(path):
            continue
        try:
            for i, line in enumerate(_iter_lines(path), start=1):
                for name, pattern in patterns:
                    if pattern.search(line):
                        findings.append(f"{path.relative_to(repo)}:{i}: matches {name}")
                        break
        except OSError:
            continue
    return findings


def audit_tracked_file_sizes(
    repo: pathlib.Path, *, max_bytes: int = 10 * 1024 * 1024
) -> list[str]:
    findings: list[str] = []
    for path in _git_ls_files(repo):
        if not path.exists():
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > max_bytes:
            findings.append(f"{path.relative_to(repo)}: {size} bytes (>{max_bytes})")
    return findings


def audit_python_compile(repo: pathlib.Path) -> list[str]:
    targets = [repo / "backend" / "src", repo / "scripts", repo / "backend" / "tests"]
    existing = [t for t in targets if t.exists()]
    if not existing:
        return ["No python targets found to compile."]

    proc = _run(
        [sys.executable, "-m", "compileall", "-q", *[str(t) for t in existing]],
        cwd=repo,
    )
    if proc.returncode != 0:
        msg = (proc.stdout + "\n" + proc.stderr).strip() or "compileall failed"
        return [msg]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="MARS architectural audit (repo hygiene checks)."
    )
    parser.add_argument("--branch", required=True, help="Branch name being audited")
    args = parser.parse_args()

    repo = _repo_root()
    print(f"MARS audit starting (branch={args.branch})")
    print(f"Repo root: {repo}")

    if os.environ.get("OPENROUTER_API_KEY"):
        print("OPENROUTER_API_KEY: present (value not displayed)")
    else:
        print("OPENROUTER_API_KEY: not set (ok for forks/PRs; agentic audit will be skipped)")

    failures: list[str] = []

    secret_findings = audit_no_committed_secrets(repo)
    if secret_findings:
        failures.append(
            "Committed secret markers detected:\n  - "
            + "\n  - ".join(secret_findings)
        )

    big_files = audit_tracked_file_sizes(repo)
    if big_files:
        failures.append("Large tracked files detected:\n  - " + "\n  - ".join(big_files))

    compile_issues = audit_python_compile(repo)
    if compile_issues:
        failures.append("Python compile issues:\n  - " + "\n  - ".join(compile_issues))

    if failures:
        print("\nAUDIT FAILED")
        for block in failures:
            print("\n" + block)
        return 2

    print("\nAUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
