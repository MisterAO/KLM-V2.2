#!/usr/bin/env python3
"""
Automatic Documentation Update Script
Runs after each commit to update relevant documentation
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


AUTO_DOC_FILES = {
    "CHANGELOG.md",
    "80-Sessions/INDEX.md",
    "60-Resources/PLAYBOOK/README.md",
}


def get_changed_files() -> List[str]:
    """Get list of files changed in the last commit"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().split("\n") if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        # If HEAD~1 doesn't exist (first commit), get staged files
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip().split("\n") if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []


def should_update_docs(changed_files: List[str]) -> bool:
    """Determine if documentation should be updated based on changed files"""
    doc_extensions = [".md", ".rst", ".txt"]
    code_extensions = [".py", ".js", ".ts"]

    for file_path in changed_files:
        if not file_path:  # Skip empty strings
            continue

        path = Path(file_path)
        if path.suffix in doc_extensions:
            return True
        if path.suffix in code_extensions:
            # Check if it's an API route or model file
            if "api" in str(path) or "models" in str(path):
                return True

    return False


def update_changelog(changed_files: List[str]):
    """Update CHANGELOG.md with recent changes"""
    changelog_path = Path("CHANGELOG.md")

    # If this commit only changes auto-generated documentation files, do not
    # create an additional changelog entry (prevents a post-commit feedback loop).
    changed = {f for f in changed_files if f}
    if changed and changed.issubset(AUTO_DOC_FILES):
        return

    # Get commit message
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s"],
            capture_output=True,
            text=True,
            check=True,
        )
        commit_message = result.stdout.strip()
    except subprocess.CalledProcessError:
        commit_message = "Updated documentation"

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Read existing changelog
    if changelog_path.exists():
        with open(changelog_path, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"

    # Add entry if not already present
    entry = f"- {current_date}: {commit_message}\n"
    if entry not in content:
        # Find the first version section or add one
        if "## [Unreleased]" in content:
            # Insert after ## [Unreleased]
            lines = content.split("\n")
            new_lines = []
            added = False
            for line in lines:
                new_lines.append(line)
                if line.strip() == "## [Unreleased]" and not added:
                    new_lines.append(entry)
                    added = True
            content = "\n".join(new_lines)
        else:
            # Add Unreleased section
            content += f"\n## [Unreleased]\n{entry}\n"

    # Write back
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(content)


def update_api_docs(changed_files: List[str]):
    """Update API documentation if API files changed"""
    api_files = [f for f in changed_files if "api" in f and f.endswith(".py")]

    if not api_files:
        return

    # This would be where we'd generate API docs
    # For now, we'll just log that API files were updated
    print(f"API files updated: {api_files}")
    print("Would generate/update API documentation here")


def update_session_logs():
    """Update session logs index"""
    sessions_dir = Path("80-Sessions")
    index_path = sessions_dir / "INDEX.md"

    if not sessions_dir.exists():
        return

    # Get all session directories
    session_dirs = []
    for item in sessions_dir.iterdir():
        if item.is_dir() and item.name != "TEMPLATES":
            session_dirs.append(item)

    if not session_dirs:
        return

    # Sort by name (which should be date-based)
    session_dirs.sort(key=lambda x: x.name, reverse=True)

    # Update index
    content = "# 📚 Session Logs Index\n\n"
    content += "> **Last Updated:** " + datetime.now().strftime("%Y-%m-%d") + "\n\n"
    content += "## 📋 Sessions\n\n"

    for session_dir in session_dirs[:20]:  # Show last 20 sessions
        # Look for SUMMARY.md or similar summary file
        summary_file = session_dir / "SUMMARY.md"
        if summary_file.exists():
            # Read title from SUMMARY.md
            with open(summary_file, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.startswith("# "):
                    title = first_line[2:]
                else:
                    title = session_dir.name
        else:
            title = session_dir.name

        content += f"- [{title}]({session_dir.name}/SUMMARY.md)\n"

    content += "\n---\n\n"
    content += "*This index is automatically updated after each commit*\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def update_playbook_index():
    """Update playbook index"""
    playbook_dir = Path("60-Resources/PLAYBOOK")

    if not playbook_dir.exists():
        return

    # Get all markdown files
    md_files = list(playbook_dir.glob("*.md"))
    md_files.sort(key=lambda x: x.name)

    if not md_files:
        return

    index_path = playbook_dir / "README.md"

    # Always rewrite index from scratch to keep the file idempotent.
    content = "# 📚 Playbook Index\n\n"
    content += "> **Last Updated:** " + datetime.now().strftime("%Y-%m-%d") + "\n\n"
    content += "## 📋 Documentation Files\n\n"

    for md_file in md_files:
        if md_file.name == "README.md":
            continue

        # Read title from file
        with open(md_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("# "):
                title = first_line[2:]
            else:
                title = md_file.stem.replace("-", " ").title()

        content += f"- [{title}]({md_file.name})\n"

    content += "\n---\n\n"
    content += "*This index is automatically updated after each commit*\n"

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    """Main function"""
    print("Checking for documentation updates...")

    changed_files = get_changed_files()

    if not changed_files or not any(changed_files):
        print("No files changed in this commit")
        return 0

    print(f"Files changed: {len(changed_files)}")
    for file_path in changed_files:
        if file_path:
            print(f"  - {file_path}")

    # Always update session logs and playbook index
    try:
        update_session_logs()
        print("Session logs index updated")
    except Exception as e:
        print(f"⚠️  Error updating session logs: {e}")

    try:
        update_playbook_index()
        print("Playbook index updated")
    except Exception as e:
        print(f"⚠️  Error updating playbook index: {e}")

    # Update changelog if needed
    if should_update_docs(changed_files):
        try:
            update_changelog(changed_files)
            print("CHANGELOG.md updated")
        except Exception as e:
            print(f"⚠️  Error updating CHANGELOG.md: {e}")

        # Update API docs if API files changed
        try:
            update_api_docs(changed_files)
            print("API documentation checked")
        except Exception as e:
            print(f"⚠️  Error updating API docs: {e}")

    print("Documentation update complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
