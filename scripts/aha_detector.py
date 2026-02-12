#!/usr/bin/env python3
"""
AHA Moment Detector

Automatically detects "AHA" moments in code, commits, and conversations,
then adds them to training documentation.

An AHA moment is when:
1. A complex problem is solved elegantly
2. A new pattern or technique is discovered
3. A significant optimization is made
4. A tricky bug is fixed with an insightful solution
5. Architecture decisions are made with clear rationale
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import argparse


@dataclass
class AHAMoment:
    """Represents an AHA moment"""

    id: str
    timestamp: str
    source: str  # 'commit', 'code', 'conversation', 'issue', 'pr'
    file_path: Optional[str]
    title: str
    description: str
    category: str  # 'pattern', 'optimization', 'bugfix', 'architecture', 'insight'
    confidence: float  # 0.0 to 1.0
    keywords: List[str]
    code_snippet: Optional[str]
    related_files: List[str]
    author: Optional[str]
    commit_hash: Optional[str]


class AHADetector:
    """Detects AHA moments from various sources"""

    # Keywords that indicate AHA moments
    AHA_KEYWORDS = {
        "pattern": [
            "pattern",
            "elegant",
            "clever",
            "insight",
            "realization",
            "discovered",
            "figured out",
            "breakthrough",
            "innovative",
        ],
        "optimization": [
            "optimized",
            "performance",
            "10x",
            "100x",
            "faster",
            "benchmark",
            "efficient",
            "reduced latency",
            "cache hit",
            "vectorized",
            "parallelized",
            "async",
            "concurrent",
        ],
        "bugfix": [
            "finally fixed",
            "root cause",
            "edge case",
            "race condition",
            "memory leak",
            "deadlock",
            "null pointer",
            "off by one",
            "the issue was",
            "turns out",
            "actually",
            "discovered that",
        ],
        "architecture": [
            "refactored",
            "restructured",
            "modularized",
            "decoupled",
            "microservice",
            "event-driven",
            "cqrs",
            "event sourcing",
            "domain-driven",
            "hexagonal",
            "clean architecture",
        ],
        "insight": [
            "aha",
            "eureka",
            "lightbulb",
            "realization",
            "understood",
            "now i see",
            "the key is",
            "the trick",
            "workaround",
            "lesson learned",
            "pro tip",
            "best practice",
        ],
    }

    # Code patterns that indicate sophisticated solutions
    CODE_PATTERNS = {
        "decorator": r"@\w+\s*\n\s*def\s+\w+",
        "context_manager": r"with\s+\w+\s*\(",
        "metaclass": r"class\s+\w+\s*\([^)]*metaclass",
        "generator": r"yield\s+",
        "coroutine": r"async\s+def|await\s+",
        "descriptor": r"__get__|__set__|__delete__",
        "singleton": r"def\s+get_instance|__new__\s*\([^)]*cls",
        "factory": r"def\s+create_|factory",
        "strategy": r"class.*Strategy|def\s+execute\w*\s*\(",
        "observer": r"attach|detach|notify|subscribe",
    }

    def __init__(
        self,
        root_path: str = ".",
        min_confidence: float = 0.7,
        keyword_threshold: int = 3,
        output_dir: str = "70-Training/best-practices",
        auto_commit: bool = False,
        review_required: bool = True,
    ):
        self.root = Path(root_path)
        self.min_confidence = min_confidence
        self.keyword_threshold = keyword_threshold
        self.output_dir = Path(output_dir)
        self.auto_commit = auto_commit
        self.review_required = review_required
        self.detected_moments: List[AHAMoment] = []

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def analyze_commit_message(
        self, message: str, commit_hash: str = None, author: str = None
    ) -> Optional[AHAMoment]:
        """Analyze a commit message for AHA moments"""
        message_lower = message.lower()

        # Count keywords per category
        category_scores = defaultdict(int)
        matched_keywords = []

        for category, keywords in self.AHA_KEYWORDS.items():
            for keyword in keywords:
                count = message_lower.count(keyword)
                if count > 0:
                    category_scores[category] += count
                    matched_keywords.append(keyword)

        # Calculate confidence
        total_keywords = sum(category_scores.values())
        if total_keywords < self.keyword_threshold:
            return None

        confidence = min(0.5 + (total_keywords * 0.1), 1.0)

        if confidence < self.min_confidence:
            return None

        # Determine primary category
        primary_category = max(category_scores, key=category_scores.get)

        # Generate title from message
        title = self._extract_title(message)

        # Create AHA moment
        moment = AHAMoment(
            id=self._generate_id(message),
            timestamp=datetime.now().isoformat(),
            source="commit",
            file_path=None,
            title=title,
            description=message.strip(),
            category=primary_category,
            confidence=round(confidence, 2),
            keywords=list(set(matched_keywords)),
            code_snippet=None,
            related_files=[],
            author=author,
            commit_hash=commit_hash,
        )

        return moment

    def analyze_code(
        self, file_path: str, content: str, author: str = None
    ) -> List[AHAMoment]:
        """Analyze code file for AHA moments"""
        moments = []

        # Check for sophisticated patterns
        for pattern_name, pattern_regex in self.CODE_PATTERNS.items():
            matches = list(
                re.finditer(pattern_regex, content, re.MULTILINE | re.IGNORECASE)
            )

            for match in matches[:3]:  # Limit to first 3 occurrences
                # Extract context
                start = max(0, match.start() - 200)
                end = min(len(content), match.end() + 200)
                snippet = content[start:end]

                # Check if it has explanatory comments
                has_explanation = self._has_good_comments(snippet)

                confidence = 0.6 if has_explanation else 0.5

                if confidence >= self.min_confidence:
                    moment = AHAMoment(
                        id=self._generate_id(f"{file_path}:{match.start()}"),
                        timestamp=datetime.now().isoformat(),
                        source="code",
                        file_path=file_path,
                        title=f"Uses {pattern_name.replace('_', ' ').title()} Pattern",
                        description=f"Sophisticated use of {pattern_name} pattern detected",
                        category="pattern",
                        confidence=round(confidence, 2),
                        keywords=[pattern_name, "pattern", "design"],
                        code_snippet=snippet.strip(),
                        related_files=[file_path],
                        author=author,
                        commit_hash=None,
                    )
                    moments.append(moment)

        # Check for optimization comments
        optimization_pattern = r"#.*?(optimized|performance|TODO.*optimize|FIXME.*slow)"
        for match in re.finditer(optimization_pattern, content, re.IGNORECASE):
            snippet = self._extract_snippet(content, match.start(), 300)

            moment = AHAMoment(
                id=self._generate_id(f"{file_path}:opt:{match.start()}"),
                timestamp=datetime.now().isoformat(),
                source="code",
                file_path=file_path,
                title="Optimization Opportunity or Solution",
                description="Code contains optimization notes or implementations",
                category="optimization",
                confidence=0.75,
                keywords=["optimization", "performance"],
                code_snippet=snippet.strip(),
                related_files=[file_path],
                author=author,
                commit_hash=None,
            )
            moments.append(moment)

        return moments

    def analyze_conversation(
        self, text: str, source: str = "conversation"
    ) -> List[AHAMoment]:
        """Analyze conversation/chat text for AHA moments"""
        moments = []

        # Split into paragraphs
        paragraphs = text.split("\n\n")

        for paragraph in paragraphs:
            para_lower = paragraph.lower()

            # Check for AHA indicators
            category_scores = defaultdict(int)
            matched_keywords = []

            for category, keywords in self.AHA_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in para_lower:
                        category_scores[category] += 1
                        matched_keywords.append(keyword)

            total_keywords = sum(category_scores.values())
            if total_keywords >= self.keyword_threshold:
                confidence = min(0.5 + (total_keywords * 0.15), 1.0)

                if confidence >= self.min_confidence:
                    primary_category = max(category_scores, key=category_scores.get)

                    moment = AHAMoment(
                        id=self._generate_id(paragraph[:100]),
                        timestamp=datetime.now().isoformat(),
                        source=source,
                        file_path=None,
                        title=self._extract_title(paragraph),
                        description=paragraph.strip(),
                        category=primary_category,
                        confidence=round(confidence, 2),
                        keywords=list(set(matched_keywords)),
                        code_snippet=None,
                        related_files=[],
                        author=None,
                        commit_hash=None,
                    )
                    moments.append(moment)

        return moments

    def scan_repository(self) -> List[AHAMoment]:
        """Scan entire repository for AHA moments"""
        print("🔍 Scanning repository for AHA moments...")

        all_moments = []

        # Scan git commits
        print("  📜 Analyzing git commits...")
        commit_moments = self._scan_git_commits()
        all_moments.extend(commit_moments)

        # Scan Python files
        print("  🐍 Analyzing Python files...")
        for py_file in self.root.rglob("*.py"):
            if ".venv" in str(py_file) or "__pycache__" in str(py_file):
                continue

            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    relative_path = str(py_file.relative_to(self.root))
                    moments = self.analyze_code(relative_path, content)
                    all_moments.extend(moments)
            except Exception as e:
                print(f"    ⚠️  Error reading {py_file}: {e}")

        # Scan Markdown files for insights
        print("  📝 Analyzing documentation...")
        for md_file in self.root.rglob("*.md"):
            if ".git" in str(md_file):
                continue

            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    relative_path = str(md_file.relative_to(self.root))
                    moments = self.analyze_conversation(content, source="documentation")
                    for m in moments:
                        m.file_path = relative_path
                    all_moments.extend(moments)
            except Exception as e:
                print(f"    ⚠️  Error reading {md_file}: {e}")

        # Remove duplicates based on ID
        seen_ids = set()
        unique_moments = []
        for moment in all_moments:
            if moment.id not in seen_ids:
                seen_ids.add(moment.id)
                unique_moments.append(moment)

        self.detected_moments = unique_moments

        print(f"✅ Found {len(unique_moments)} AHA moments")
        return unique_moments

    def _scan_git_commits(self) -> List[AHAMoment]:
        """Scan git commits for AHA moments"""
        moments = []

        try:
            import subprocess

            # Get recent commits
            result = subprocess.run(
                ["git", "log", "--format=%H|%an|%s|%b", "-n", "50"],
                capture_output=True,
                text=True,
                cwd=self.root,
            )

            if result.returncode == 0:
                commits = result.stdout.strip().split("\n\n")

                for commit_block in commits:
                    lines = commit_block.split("\n")
                    if lines and "|" in lines[0]:
                        parts = lines[0].split("|", 3)
                        if len(parts) >= 3:
                            commit_hash = parts[0]
                            author = parts[1]
                            message = parts[2]
                            body = parts[3] if len(parts) > 3 else ""

                            full_message = f"{message}\n{body}".strip()

                            moment = self.analyze_commit_message(
                                full_message, commit_hash=commit_hash[:8], author=author
                            )

                            if moment:
                                moments.append(moment)

        except Exception as e:
            print(f"    ⚠️  Could not scan git commits: {e}")

        return moments

    def _generate_id(self, content: str) -> str:
        """Generate unique ID for AHA moment"""
        hash_obj = hashlib.md5(content.encode())
        return hash_obj.hexdigest()[:12]

    def _extract_title(self, text: str) -> str:
        """Extract a title from text"""
        lines = text.strip().split("\n")
        first_line = lines[0] if lines else text

        # Clean up title
        title = first_line.strip()
        title = re.sub(r"^\s*[-*#]+\s*", "", title)  # Remove markdown markers
        title = re.sub(r"\s+", " ", title)  # Normalize whitespace

        # Limit length
        if len(title) > 100:
            title = title[:97] + "..."

        return title if title else "AHA Moment"

    def _extract_snippet(self, content: str, position: int, context: int = 300) -> str:
        """Extract code snippet around position"""
        start = max(0, position - context)
        end = min(len(content), position + context)
        return content[start:end]

    def _has_good_comments(self, code: str) -> bool:
        """Check if code has explanatory comments"""
        comment_patterns = [
            r"#\s*(?:TODO|FIXME|NOTE|HACK|XXX|BUG)",
            r'""".*?"""',
            r"'''.*?'''",
            r"//\s*\w+",
            r"/\*.*?\*/",
        ]

        for pattern in comment_patterns:
            if re.search(pattern, code, re.DOTALL | re.IGNORECASE):
                return True

        return False

    def generate_training_doc(self) -> str:
        """Generate training documentation from detected AHA moments"""
        if not self.detected_moments:
            return "# AHA Moments Archive\n\nNo AHA moments detected yet.\n"

        lines = [
            "# 💡 AHA Moments Archive",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Moments:** {len(self.detected_moments)}",
            "",
            "This document contains insights, patterns, and breakthrough moments discovered during development.",
            "",
            "---",
            "",
        ]

        # Group by category
        by_category = defaultdict(list)
        for moment in self.detected_moments:
            by_category[moment.category].append(moment)

        # Generate sections
        for category in sorted(by_category.keys()):
            moments = by_category[category]
            category_icon = {
                "pattern": "🎯",
                "optimization": "⚡",
                "bugfix": "🐛",
                "architecture": "🏗️",
                "insight": "💡",
            }.get(category, "📝")

            lines.extend([f"## {category_icon} {category.upper()}", ""])

            # Sort by confidence
            for moment in sorted(moments, key=lambda m: m.confidence, reverse=True):
                lines.extend(self._format_moment(moment))
                lines.append("")

        lines.extend(
            [
                "---",
                "",
                "*This document is auto-generated by `scripts/aha_detector.py`*",
            ]
        )

        return "\n".join(lines)

    def _format_moment(self, moment: AHAMoment) -> List[str]:
        """Format a single AHA moment for documentation"""
        lines = [
            f"### {moment.title}",
            "",
            f"**ID:** `{moment.id}`  ",
            f"**Confidence:** {'⭐' * int(moment.confidence * 5)} ({moment.confidence:.0%})  ",
            f"**Source:** {moment.source}  ",
            f"**Detected:** {moment.timestamp[:10]}",
        ]

        if moment.author:
            lines.append(f"**Author:** {moment.author}  ")

        if moment.file_path:
            lines.append(f"**File:** `{moment.file_path}`  ")

        if moment.commit_hash:
            lines.append(f"**Commit:** `{moment.commit_hash}`  ")

        lines.extend(
            [
                "",
                f"**Keywords:** {', '.join(moment.keywords)}",
                "",
                "**Description:**",
                "",
                f"> {moment.description}",
            ]
        )

        if moment.code_snippet:
            lines.extend(["", "**Code:**", "", "```python", moment.code_snippet, "```"])

        if moment.related_files:
            lines.extend(["", "**Related Files:**", ""])
            for f in moment.related_files:
                lines.append(f"- `{f}`")

        return lines

    def save(self, output_file: str = "AHA_MOMENTS.md"):
        """Save detected AHA moments to file"""
        output_path = self.output_dir / output_file
        content = self.generate_training_doc()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ AHA moments saved to: {output_path}")

        # Also save as JSON for programmatic access
        json_path = self.output_dir / "aha_moments.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([asdict(m) for m in self.detected_moments], f, indent=2)

        print(f"✅ JSON data saved to: {json_path}")

        return output_path

    def review_pending(self) -> List[AHAMoment]:
        """Get moments pending review"""
        return [m for m in self.detected_moments if m.confidence >= 0.8]


def main():
    parser = argparse.ArgumentParser(
        description="Detect AHA moments and add to training docs"
    )
    parser.add_argument("--root", "-r", default=".", help="Root directory to scan")
    parser.add_argument(
        "--output-dir",
        "-o",
        default="70-Training/best-practices",
        help="Output directory for training docs",
    )
    parser.add_argument(
        "--min-confidence",
        "-c",
        type=float,
        default=0.7,
        help="Minimum confidence threshold (0.0-1.0)",
    )
    parser.add_argument(
        "--keyword-threshold", "-k", type=int, default=3, help="Minimum keyword matches"
    )
    parser.add_argument(
        "--auto-commit", action="store_true", help="Automatically commit AHA moments"
    )
    parser.add_argument("--file", "-f", help="Analyze specific file for AHA moments")
    parser.add_argument("--message", "-m", help="Analyze commit message")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    detector = AHADetector(
        root_path=args.root,
        min_confidence=args.min_confidence,
        keyword_threshold=args.keyword_threshold,
        output_dir=args.output_dir,
        auto_commit=args.auto_commit,
    )

    if args.message:
        # Analyze single message
        moment = detector.analyze_commit_message(args.message)
        if moment:
            if args.json:
                print(json.dumps(asdict(moment), indent=2))
            else:
                print(f"✅ AHA Moment Detected!")
                print(f"   Title: {moment.title}")
                print(f"   Category: {moment.category}")
                print(f"   Confidence: {moment.confidence:.0%}")
                print(f"   Keywords: {', '.join(moment.keywords)}")
        else:
            print("❌ No AHA moment detected in message")

    elif args.file:
        # Analyze single file
        with open(args.file, "r") as f:
            content = f.read()
        moments = detector.analyze_code(args.file, content)

        if moments:
            print(f"✅ Found {len(moments)} AHA moments in {args.file}")
            if args.json:
                print(json.dumps([asdict(m) for m in moments], indent=2))
        else:
            print(f"❌ No AHA moments detected in {args.file}")

    else:
        # Scan entire repository
        detector.scan_repository()

        if detector.detected_moments:
            detector.save()

            high_confidence = detector.review_pending()
            if high_confidence:
                print(
                    f"\n⭐ High-confidence moments pending review: {len(high_confidence)}"
                )
        else:
            print("\nNo AHA moments detected in repository")


if __name__ == "__main__":
    main()
