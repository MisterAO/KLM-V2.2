#!/usr/bin/env python3
"""
Agent Documentation Maintenance Script
Used by agents to automatically maintain their documentation
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class AgentDocumentationManager:
    """Manages documentation for AI agents"""

    def __init__(self, agent_id: str, agent_name: str):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.docs_dir = Path("60-Resources/PLAYBOOK")
        self.journal_dir = Path("70-Training/journal")
        self.session_dir = Path("80-Sessions")

    def update_agent_journal(self, entry: str, entry_type: str = "general"):
        """Update agent's journal with a new entry"""
        journal_file = self.journal_dir / f"{self.agent_id}_journal.md"

        # Create journal directory if it doesn't exist
        self.journal_dir.mkdir(parents=True, exist_ok=True)

        # Create or update journal
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if journal_file.exists():
            with open(journal_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = f"# {self.agent_name} ({self.agent_id}) Journal\n\n"
            content += f"> **Started:** {datetime.now().strftime('%Y-%m-%d')}\n\n"

        # Add new entry
        new_entry = f"\n## 📝 {timestamp} - {entry_type.title()}\n\n{entry}\n"
        content += new_entry

        with open(journal_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Journal updated for {self.agent_name}")

    def update_agent_sop(self, content: str, sop_name: Optional[str] = None):
        """Update or create agent's SOP"""
        if sop_name is None:
            sop_name = f"AGENT-{self.agent_id.replace('AGT-', '')}"

        sop_file = Path("40-SOPs/AGENTS") / f"{sop_name}.md"

        # Create directory if it doesn't exist
        sop_file.parent.mkdir(parents=True, exist_ok=True)

        # Update SOP
        with open(sop_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ SOP updated: {sop_name}")

    def log_decision(self, decision: str, context: str, outcome: str):
        """Log a decision made by the agent"""
        decisions_file = self.docs_dir / "02-DECISION_LOG.md"

        # Create decisions file if it doesn't exist
        if not decisions_file.exists():
            with open(decisions_file, "w", encoding="utf-8") as f:
                f.write("# 📝 Decision Log\n\n")
                f.write("> **Tracking key decisions made during development**\n\n")

        # Read existing content
        with open(decisions_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add new decision
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = f"\n## 🤖 {self.agent_name} Decision - {timestamp}\n\n"
        new_entry += f"**Decision:** {decision}\n\n"
        new_entry += f"**Context:** {context}\n\n"
        new_entry += f"**Outcome:** {outcome}\n\n"
        new_entry += "---\n"

        content += new_entry

        # Write back
        with open(decisions_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Decision logged for {self.agent_name}")

    def log_roadblock(self, problem: str, solution: str, impact: str):
        """Log a roadblock and its solution"""
        roadblocks_file = self.docs_dir / "03-ROADBLOCKS.md"

        # Create roadblocks file if it doesn't exist
        if not roadblocks_file.exists():
            with open(roadblocks_file, "w", encoding="utf-8") as f:
                f.write("# 🚧 Roadblocks & Solutions\n\n")
                f.write("> **Documenting challenges and how we solved them**\n\n")

        # Read existing content
        with open(roadblocks_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add new roadblock
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = f"\n## 🤖 {self.agent_name} - {timestamp}\n\n"
        new_entry += f"**Problem:** {problem}\n\n"
        new_entry += f"**Solution:** {solution}\n\n"
        new_entry += f"**Impact:** {impact}\n\n"
        new_entry += "---\n"

        content += new_entry

        # Write back
        with open(roadblocks_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Roadblock logged for {self.agent_name}")

    def add_tips_and_tricks(self, tip: str, category: str):
        """Add tips and tricks learned by the agent"""
        tips_file = self.docs_dir / "07-TIPS_TRICKS.md"

        # Create tips file if it doesn't exist
        if not tips_file.exists():
            with open(tips_file, "w", encoding="utf-8") as f:
                f.write("# 💡 Tips & Tricks\n\n")
                f.write(
                    "> **Best practices and insights learned during development**\n\n"
                )

        # Read existing content
        with open(tips_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add new tip
        timestamp = datetime.now().strftime("%Y-%m-%d")
        new_entry = f"\n## 🤖 {self.agent_name} - {category.title()} ({timestamp})\n\n"
        new_entry += f"{tip}\n\n"
        new_entry += "---\n"

        content += new_entry

        # Write back
        with open(tips_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Tip added for {self.agent_name}")


def main():
    """Main function - can be called by agents"""
    if len(sys.argv) < 2:
        print("Usage: python agent_docs.py <agent_id> <agent_name> [command] [args...]")
        print("Commands:")
        print("  journal <entry> [type]     - Add journal entry")
        print("  decision <decision> <context> <outcome> - Log decision")
        print("  roadblock <problem> <solution> <impact> - Log roadblock")
        print("  tip <tip> <category>       - Add tip")
        return 1

    agent_id = sys.argv[1]
    agent_name = sys.argv[2] if len(sys.argv) > 2 else agent_id

    manager = AgentDocumentationManager(agent_id, agent_name)

    if len(sys.argv) < 4:
        print("Missing command and arguments")
        return 1

    command = sys.argv[3]

    if command == "journal" and len(sys.argv) >= 5:
        entry = sys.argv[4]
        entry_type = sys.argv[5] if len(sys.argv) > 5 else "general"
        manager.update_agent_journal(entry, entry_type)
    elif command == "decision" and len(sys.argv) >= 7:
        decision = sys.argv[4]
        context = sys.argv[5]
        outcome = sys.argv[6]
        manager.log_decision(decision, context, outcome)
    elif command == "roadblock" and len(sys.argv) >= 7:
        problem = sys.argv[4]
        solution = sys.argv[5]
        impact = sys.argv[6]
        manager.log_roadblock(problem, solution, impact)
    elif command == "tip" and len(sys.argv) >= 6:
        tip = sys.argv[4]
        category = sys.argv[5]
        manager.add_tips_and_tricks(tip, category)
    else:
        print(f"Unknown command or missing arguments for: {command}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
