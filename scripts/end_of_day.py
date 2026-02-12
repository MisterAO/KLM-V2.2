#!/usr/bin/env python3
"""
End-of-Day Refactoring and Documentation Script
Performs comprehensive code quality checks and documentation updates
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


def run_command(
    command: List[str], cwd: Optional[str] = None
) -> subprocess.CompletedProcess:
    """Run a command and return the result"""
    try:
        return subprocess.run(
            command, capture_output=True, text=True, cwd=cwd, check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Command failed: {' '.join(command)}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return e


def check_code_quality():
    """Run code quality checks"""
    print("🔍 Running code quality checks...")

    # Check if we're in a Python project
    if not Path("pyproject.toml").exists() and not Path("requirements.txt").exists():
        print("⚠️  No Python project files found, skipping Python checks")
        return

    # Run black formatting check
    print("  🖌️  Checking code formatting (black)...")
    try:
        result = run_command([sys.executable, "-m", "black", "--check", "backend/src"])
        if result.returncode == 0:
            print("    ✅ Code is properly formatted")
        else:
            print("    ⚠️  Code formatting issues found")
    except Exception as e:
        print(f"    ⚠️  Error running black: {e}")

    # Run isort import sorting check
    print("  📦 Checking import sorting (isort)...")
    try:
        result = run_command(
            [sys.executable, "-m", "isort", "--check-only", "backend/src"]
        )
        if result.returncode == 0:
            print("    ✅ Imports are properly sorted")
        else:
            print("    ⚠️  Import sorting issues found")
    except Exception as e:
        print(f"    ⚠️  Error running isort: {e}")

    # Run ruff linting
    print("  🐶 Checking code linting (ruff)...")
    try:
        result = run_command([sys.executable, "-m", "ruff", "check", "backend/src"])
        if result.returncode == 0:
            print("    ✅ No linting issues found")
        else:
            print("    ⚠️  Linting issues found")
    except Exception as e:
        print(f"    ⚠️  Error running ruff: {e}")

    # Run mypy type checking
    print("  🔍 Checking type hints (mypy)...")
    try:
        result = run_command([sys.executable, "-m", "mypy", "backend/src"])
        if result.returncode == 0:
            print("    ✅ No type checking issues found")
        else:
            print("    ⚠️  Type checking issues found")
    except Exception as e:
        print(f"    ⚠️  Error running mypy: {e}")


def run_tests():
    """Run tests and generate coverage report"""
    print("🧪 Running tests...")

    # Check if we have tests
    if not Path("backend/tests").exists():
        print("⚠️  No tests directory found, skipping tests")
        return

    # Run tests
    print("  ▶️  Running unit tests...")
    try:
        result = run_command([sys.executable, "-m", "pytest", "backend/tests", "-v"])
        if result.returncode == 0:
            print("    ✅ All tests passed")
        else:
            print("    ❌ Some tests failed")
            print(result.stdout)
    except Exception as e:
        print(f"    ⚠️  Error running tests: {e}")


def update_documentation():
    """Update all documentation"""
    print("📚 Updating documentation...")

    # Update CHANGELOG.md
    print("  📝 Updating CHANGELOG.md...")
    try:
        result = run_command([sys.executable, "scripts/update_docs.py"])
        if result.returncode == 0:
            print("    ✅ Documentation updated")
        else:
            print("    ⚠️  Documentation update had issues")
    except Exception as e:
        print(f"    ⚠️  Error updating documentation: {e}")

    # Update API documentation
    print("  📖 Updating API documentation...")
    # This would be where we'd generate API docs from code
    print("    ℹ️  API documentation would be generated here")


def generate_code_metrics():
    """Generate code metrics and statistics"""
    print("📊 Generating code metrics...")

    # Count lines of code
    try:
        result = run_command(
            ["find", "backend/src", "-name", "*.py", "-exec", "wc", "-l", "{}", "+"]
        )
        if result.returncode == 0:
            lines = 0
            for line in result.stdout.split("\n"):
                if line.strip() and not line.endswith("total"):
                    parts = line.strip().split()
                    if parts and parts[0].isdigit():
                        lines += int(parts[0])
            print(f"    📏 Total Python lines: {lines}")
    except Exception as e:
        print(f"    ⚠️  Error counting lines: {e}")

    # Count test files
    try:
        result = run_command(
            ["find", "backend/tests", "-name", "*.py", "-exec", "ls", "{}", "+"]
        )
        if result.returncode == 0:
            test_files = len(
                [line for line in result.stdout.split("\n") if line.strip()]
            )
            print(f"    🧪 Test files: {test_files}")
    except Exception as e:
        print(f"    ⚠️  Error counting test files: {e}")


def update_project_dashboard():
    """Update project dashboard with current status"""
    print("📋 Updating project dashboard...")

    dashboard_path = Path("PROJECT_DASHBOARD.md")

    if not dashboard_path.exists():
        print("    ⚠️  Project dashboard not found")
        return

    # Read current dashboard
    with open(dashboard_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update timestamp
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated_content = content.replace(
        "> **Last Updated:**", f"> **Last Updated:** {current_date}"
    )

    # If no replacement was made, add the timestamp
    if updated_content == content:
        lines = content.split("\n")
        if len(lines) > 1:
            lines.insert(1, f"> **Last Updated:** {current_date}")
            updated_content = "\n".join(lines)

    # Write back
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("    ✅ Project dashboard updated")


def main():
    """Main function"""
    print("🌅 KLM V2 End-of-Day Refactoring and Documentation")
    print("=" * 50)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print()

    # Run all checks and updates
    check_code_quality()
    print()

    run_tests()
    print()

    update_documentation()
    print()

    generate_code_metrics()
    print()

    update_project_dashboard()
    print()

    print("✨ End-of-Day processing complete!")
    print("💡 Remember to review any changes and commit them")

    return 0


if __name__ == "__main__":
    sys.exit(main())
