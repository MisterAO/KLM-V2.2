#!/usr/bin/env python3
"""Generate a V2 -> V2.1 rebuild report.

This produces a single markdown artifact that shows what changed between two git
refs (defaults: master -> v2.1) and where the decision/SOP/session audit trail
lives in the repo.

Outputs:
- 90-Project-Board/DASHBOARD_DATA/v2_to_v21_report.md
"""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class CompareResult:
    generated_at_utc: str
    base_ref: str
    target_ref: str
    base_sha: str
    target_sha: str
    commit_list: list[str]
    diff_stat: str
    diff_name_status: list[str]


def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = (completed.stdout or "").rstrip()
    stderr = (completed.stderr or "").rstrip()
    if completed.returncode != 0:
        message = f"Command failed ({completed.returncode}): {' '.join(command)}"
        if stderr:
            message += f"\n{stderr}"
        raise RuntimeError(message)
    return stdout


def _safe_lines(output: str) -> list[str]:
    return [line.rstrip() for line in output.splitlines() if line.strip()]


def _rev_parse(ref: str) -> str:
    return _run(["git", "rev-parse", ref]).strip()


def compare(base_ref: str, target_ref: str) -> CompareResult:
    generated_at_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base_sha = _rev_parse(base_ref)
    target_sha = _rev_parse(target_ref)

    commit_list = _safe_lines(
        _run(["git", "log", "--oneline", f"{base_ref}..{target_ref}"])
    )
    diff_stat = _run(["git", "diff", "--stat", f"{base_ref}...{target_ref}"])
    diff_name_status = _safe_lines(
        _run(["git", "diff", "--name-status", f"{base_ref}...{target_ref}"])
    )

    return CompareResult(
        generated_at_utc=generated_at_utc,
        base_ref=base_ref,
        target_ref=target_ref,
        base_sha=base_sha,
        target_sha=target_sha,
        commit_list=commit_list,
        diff_stat=diff_stat,
        diff_name_status=diff_name_status,
    )


def _bucket_paths(diff_name_status: list[str], prefix: str) -> list[str]:
    out: list[str] = []
    for line in diff_name_status:
        # Format is: <STATUS>\t<PATH>
        parts = line.split("\t", 1)
        if len(parts) != 2:
            continue
        path = parts[1]
        if path.startswith(prefix):
            out.append(line)
    return out


def render_markdown(result: CompareResult) -> str:
    lines: list[str] = []
    lines.append("# V2 → V2.1 Rebuild Report")
    lines.append("")
    lines.append(f"**Generated (UTC):** {result.generated_at_utc}")
    lines.append(f"**Base (V2):** `{result.base_ref}` @ `{result.base_sha[:12]}`")
    lines.append(f"**Target (V2.1):** `{result.target_ref}` @ `{result.target_sha[:12]}`")
    lines.append("")

    lines.append("## What this proves")
    lines.append(
        "This file is a deterministic, repo-derived summary of what changed between V2 and V2.1. "
        "It is meant to accompany the detailed audit trail in session logs, SOPs, and decision logs."
    )
    lines.append("")

    lines.append("## Key audit trail locations")
    lines.append("- SOP catalog: `40-SOPs/SOP_INDEX.md`")
    lines.append("- Workflow SOPs (including Git+Docs sync): `40-SOPs/WORKFLOWS/`")
    lines.append("- Cross-chat decision log: `90-Project-Board/DECISION_LOG.md`")
    lines.append("- Session master index: `80-Sessions/INDEX.md`")
    lines.append("- Session folders (full logs, decisions, metrics): `80-Sessions/YYYY-MM/...`")
    lines.append("- Project tracker (what was done when): `90-Project-Board/SPRINT_TRACKER.md`")
    lines.append("")

    lines.append("## Commits (V2 → V2.1)")
    if result.commit_list:
        lines.append("```")
        lines.extend(result.commit_list)
        lines.append("```")
    else:
        lines.append("(No commits found between these refs.)")
    lines.append("")

    lines.append("## Diff summary (stat)")
    lines.append("```")
    lines.append(result.diff_stat or "(empty)")
    lines.append("```")
    lines.append("")

    lines.append("## Diff summary (name-status)")
    if result.diff_name_status:
        lines.append("```")
        lines.extend(result.diff_name_status)
        lines.append("```")
    else:
        lines.append("(No file changes found.)")
    lines.append("")

    lines.append("## Change buckets (quick navigation)")
    buckets = [
        ("SOPs", "40-SOPs/"),
        ("Session logs", "80-Sessions/"),
        ("Project board", "90-Project-Board/"),
        ("Backend", "backend/"),
        ("Implementation", "30-Implementation/"),
        ("Architecture", "20-Architecture/"),
        ("Docs", "docs/"),
        ("Exports", "export_chat/"),
        ("CI/Workflows", ".github/"),
        ("Tooling", "scripts/"),
    ]
    for title, prefix in buckets:
        bucket_lines = _bucket_paths(result.diff_name_status, prefix)
        if not bucket_lines:
            continue
        lines.append(f"### {title} ({prefix})")
        lines.append("```")
        lines.extend(bucket_lines)
        lines.append("```")
        lines.append("")

    lines.append("## How to reproduce")
    lines.append("```bash")
    lines.append(f"git fetch --all --prune")
    lines.append(f"git diff --stat {result.base_ref}...{result.target_ref}")
    lines.append(f"git diff --name-status {result.base_ref}...{result.target_ref}")
    lines.append(f"git log --oneline {result.base_ref}..{result.target_ref}")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def write_report(markdown: str) -> Path:
    out_dir = Path("90-Project-Board") / "DASHBOARD_DATA"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "v2_to_v21_report.md"
    out_path.write_text(markdown, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="master", help="Base ref (V2)")
    parser.add_argument("--target", default="v2.1", help="Target ref (V2.1)")
    args = parser.parse_args()

    result = compare(args.base, args.target)
    report_path = write_report(render_markdown(result))
    print(f"Wrote: {report_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
