#!/usr/bin/env python3
"""Codebase change tracker report generator.

Generates a lightweight markdown + JSON summary of the current repository state.

Primary use:
- Human/agent visibility into what changed
- Handoff context and planning inputs for PM-Agent

Outputs:
- 90-Project-Board/DASHBOARD_DATA/codebase_change_report.md
- 90-Project-Board/DASHBOARD_DATA/codebase_change_summary.json
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class GitSnapshot:
    generated_at_utc: str
    branch: str
    status_porcelain: list[str]
    diff_name_status: list[str]
    recent_commits: list[str]


def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()

    if completed.returncode != 0:
        message = f"Command failed ({completed.returncode}): {' '.join(command)}"
        if stderr:
            message += f"\n{stderr}"
        raise RuntimeError(message)

    return stdout


def _safe_run_lines(command: list[str]) -> list[str]:
    stdout = _run(command)
    if not stdout:
        return []
    return [line.rstrip() for line in stdout.splitlines() if line.strip()]


def get_git_snapshot() -> GitSnapshot:
    generated_at_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "unknown"

    status_porcelain = _safe_run_lines(["git", "status", "--porcelain"])
    diff_name_status = _safe_run_lines(["git", "diff", "--name-status"])

    # If the repo has no commits, this will fail; treat as empty.
    try:
        recent_commits = _safe_run_lines(["git", "log", "-n", "20", "--oneline"])
    except RuntimeError:
        recent_commits = []

    return GitSnapshot(
        generated_at_utc=generated_at_utc,
        branch=branch,
        status_porcelain=status_porcelain,
        diff_name_status=diff_name_status,
        recent_commits=recent_commits,
    )


def render_markdown(snapshot: GitSnapshot) -> str:
    changed_files = [line.split("\t", 1)[-1] for line in snapshot.diff_name_status]

    lines: list[str] = []
    lines.append("# Codebase Change Report")
    lines.append("")
    lines.append(f"**Generated (UTC):** {snapshot.generated_at_utc}")
    lines.append(f"**Branch:** {snapshot.branch}")
    lines.append("")

    lines.append("## Working Tree")
    if snapshot.status_porcelain:
        lines.append("Uncommitted changes detected:")
        lines.append("```")
        lines.extend(snapshot.status_porcelain)
        lines.append("```")
    else:
        lines.append("Working tree clean.")

    lines.append("")
    lines.append("## Diff (name-status)")
    if snapshot.diff_name_status:
        lines.append("```")
        lines.extend(snapshot.diff_name_status)
        lines.append("```")
    else:
        lines.append("No unstaged diff.")

    lines.append("")
    lines.append("## Changed Files (from diff)")
    if changed_files:
        for path in changed_files:
            lines.append(f"- {path}")
    else:
        lines.append("- (none)")

    lines.append("")
    lines.append("## Recent Commits")
    if snapshot.recent_commits:
        lines.append("```")
        lines.extend(snapshot.recent_commits)
        lines.append("```")
    else:
        lines.append("No commit history available (repo may be newly initialized).")

    lines.append("")
    return "\n".join(lines)


def write_outputs(snapshot: GitSnapshot) -> tuple[Path, Path]:
    out_dir = Path("90-Project-Board") / "DASHBOARD_DATA"
    out_dir.mkdir(parents=True, exist_ok=True)

    report_path = out_dir / "codebase_change_report.md"
    summary_path = out_dir / "codebase_change_summary.json"

    report_path.write_text(render_markdown(snapshot), encoding="utf-8")
    summary_path.write_text(json.dumps(asdict(snapshot), indent=2), encoding="utf-8")

    return report_path, summary_path


def main() -> int:
    snapshot = get_git_snapshot()
    report_path, summary_path = write_outputs(snapshot)
    print(f"Wrote: {report_path}")
    print(f"Wrote: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
