#!/usr/bin/env python3
"""
Project Map Generator - Auto-generates PROJECT_MAP.md
Creates both text structure and Mermaid diagrams
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
import argparse


@dataclass
class FileInfo:
    """Represents a file in the project"""

    path: Path
    relative_path: str
    size: int
    extension: str
    line_count: int
    is_test: bool
    is_config: bool
    is_documentation: bool
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)


@dataclass
class DirectoryInfo:
    """Represents a directory in the project"""

    path: Path
    relative_path: str
    files: List[FileInfo] = field(default_factory=list)
    subdirs: List["DirectoryInfo"] = field(default_factory=list)
    file_count: int = 0
    total_lines: int = 0


class ProjectMapGenerator:
    """Generates comprehensive project documentation"""

    # Directories to exclude
    EXCLUDE_DIRS = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".pytest_cache",
        ".mypy_cache",
        "dist",
        "build",
        ".idea",
        ".vscode",
        "coverage",
        "htmlcov",
        ".tox",
        "target",
        ".next",
        "out",
        ".turbo",
        "playwright-report",
    }

    # File extensions to include
    INCLUDE_EXTENSIONS = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".go",
        ".rs",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".cs",
        ".rb",
        ".php",
        ".swift",
        ".kt",
        ".scala",
        ".r",
        ".m",
        ".mm",
        ".sql",
        ".md",
        ".yml",
        ".yaml",
        ".json",
        ".toml",
        ".ini",
        ".cfg",
        ".dockerfile",
        ".sh",
        ".ps1",
        ".html",
        ".css",
        ".scss",
        ".less",
    }

    def __init__(self, root_path: str, output_path: str = "PROJECT_MAP.md"):
        self.root = Path(root_path).resolve()
        self.output_path = Path(output_path)
        self.tree = None
        self.metrics = {}

    def scan_project(self) -> DirectoryInfo:
        """Recursively scan the project directory"""
        print(f"🔍 Scanning project at: {self.root}")
        self.tree = self._scan_directory(self.root, "")
        print(f"✅ Scan complete. Found {self.tree.file_count} files")
        return self.tree

    def _scan_directory(self, path: Path, relative_path: str) -> DirectoryInfo:
        """Recursively scan a directory"""
        dir_info = DirectoryInfo(path=path, relative_path=relative_path)

        try:
            for item in sorted(path.iterdir()):
                # Skip excluded directories
                if item.is_dir() and item.name in self.EXCLUDE_DIRS:
                    continue

                if item.is_dir():
                    # Recursively scan subdirectory
                    sub_relative = (
                        f"{relative_path}/{item.name}" if relative_path else item.name
                    )
                    subdir = self._scan_directory(item, sub_relative)
                    if subdir.files or subdir.subdirs:  # Only include non-empty dirs
                        dir_info.subdirs.append(subdir)
                        dir_info.file_count += subdir.file_count
                        dir_info.total_lines += subdir.total_lines

                elif item.is_file():
                    file_info = self._analyze_file(item, relative_path)
                    if file_info:
                        dir_info.files.append(file_info)
                        dir_info.file_count += 1
                        dir_info.total_lines += file_info.line_count
        except PermissionError:
            print(f"⚠️  Permission denied: {path}")

        return dir_info

    def _analyze_file(self, path: Path, relative_dir: str) -> Optional[FileInfo]:
        """Analyze a single file"""
        ext = path.suffix.lower()

        # Skip binary and certain files
        if ext not in self.INCLUDE_EXTENSIONS and path.name not in [
            "Dockerfile",
            "Makefile",
        ]:
            return None

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")
                line_count = len(lines)

                # Detect file type
                is_test = "test" in path.name.lower() or "spec" in path.name.lower()
                is_config = path.name in [
                    "package.json",
                    "tsconfig.json",
                    "pyproject.toml",
                    "setup.py",
                    "requirements.txt",
                    "Cargo.toml",
                    "go.mod",
                    "pom.xml",
                    "build.gradle",
                    ".env",
                    "docker-compose.yml",
                    "Dockerfile",
                    "Makefile",
                ] or ext in [".yml", ".yaml", ".toml", ".ini", ".cfg"]
                is_doc = (
                    ext == ".md" or "README" in path.name or "CHANGELOG" in path.name
                )

                # Extract imports (language-specific)
                imports = self._extract_imports(content, ext)

                relative_path = (
                    f"{relative_dir}/{path.name}" if relative_dir else path.name
                )

                return FileInfo(
                    path=path,
                    relative_path=relative_path,
                    size=path.stat().st_size,
                    extension=ext,
                    line_count=line_count,
                    is_test=is_test,
                    is_config=is_config,
                    is_documentation=is_doc,
                    imports=imports,
                )
        except Exception as e:
            print(f"⚠️  Error reading {path}: {e}")
            return None

    def _extract_imports(self, content: str, ext: str) -> List[str]:
        """Extract import statements from file content"""
        imports = []

        if ext == ".py":
            # Python imports
            patterns = [r"^import\s+([\w.]+)", r"^from\s+([\w.]+)\s+import"]
        elif ext in [".js", ".ts", ".jsx", ".tsx"]:
            # JavaScript/TypeScript imports
            patterns = [
                r'^import\s+.*?\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'^require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            ]
        elif ext == ".go":
            # Go imports
            patterns = [r'^import\s+[\'"]([^\'"]+)[\'"]']
        elif ext == ".rs":
            # Rust imports
            patterns = [r"^use\s+([\w:]+)"]
        else:
            return imports

        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            imports.extend(matches)

        return imports

    def calculate_metrics(self) -> Dict:
        """Calculate project metrics"""
        if not self.tree:
            self.scan_project()

        metrics = {
            "total_files": 0,
            "total_lines": 0,
            "total_size": 0,
            "languages": {},
            "file_types": {"source": 0, "test": 0, "config": 0, "documentation": 0},
        }

        self._collect_metrics(self.tree, metrics)

        # Calculate percentages
        total = metrics["total_files"]
        if total > 0:
            for lang, count in metrics["languages"].items():
                metrics["languages"][lang]["percentage"] = round(
                    count["count"] / total * 100, 2
                )

        self.metrics = metrics
        return metrics

    def _collect_metrics(self, dir_info: DirectoryInfo, metrics: Dict):
        """Recursively collect metrics"""
        for file_info in dir_info.files:
            metrics["total_files"] += 1
            metrics["total_lines"] += file_info.line_count
            metrics["total_size"] += file_info.size

            # Language stats
            lang = self._get_language(file_info.extension)
            if lang not in metrics["languages"]:
                metrics["languages"][lang] = {"count": 0, "lines": 0}
            metrics["languages"][lang]["count"] += 1
            metrics["languages"][lang]["lines"] += file_info.line_count

            # File type stats
            if file_info.is_test:
                metrics["file_types"]["test"] += 1
            elif file_info.is_config:
                metrics["file_types"]["config"] += 1
            elif file_info.is_documentation:
                metrics["file_types"]["documentation"] += 1
            else:
                metrics["file_types"]["source"] += 1

        for subdir in dir_info.subdirs:
            self._collect_metrics(subdir, metrics)

    def _get_language(self, ext: str) -> str:
        """Map file extension to language name"""
        mapping = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".tsx": "TypeScript (React)",
            ".jsx": "JavaScript (React)",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".cpp": "C++",
            ".c": "C",
            ".h": "C/C++ Header",
            ".hpp": "C++ Header",
            ".cs": "C#",
            ".rb": "Ruby",
            ".php": "PHP",
            ".swift": "Swift",
            ".kt": "Kotlin",
            ".scala": "Scala",
            ".r": "R",
            ".m": "Objective-C",
            ".mm": "Objective-C++",
            ".sql": "SQL",
            ".md": "Markdown",
            ".yml": "YAML",
            ".yaml": "YAML",
            ".json": "JSON",
            ".toml": "TOML",
            ".ini": "INI",
            ".cfg": "Config",
            ".html": "HTML",
            ".css": "CSS",
            ".scss": "SCSS",
            ".less": "LESS",
        }
        return mapping.get(ext, "Other")

    def generate_text_tree(self, dir_info: DirectoryInfo, level: int = 0) -> str:
        """Generate ASCII tree structure"""
        indent = "  " * level
        output = []

        # Directory name
        name = dir_info.path.name or self.root.name
        output.append(f"{indent}📁 {name}/")

        # Files
        for file_info in sorted(dir_info.files, key=lambda f: f.path.name):
            icon = self._get_file_icon(file_info)
            size_kb = file_info.size / 1024
            output.append(
                f"{indent}  {icon} {file_info.path.name} ({file_info.line_count} lines, {size_kb:.1f} KB)"
            )

        # Subdirectories
        for subdir in dir_info.subdirs:
            output.append(self.generate_text_tree(subdir, level + 1))

        return "\n".join(output)

    def _get_file_icon(self, file_info: FileInfo) -> str:
        """Get appropriate icon for file type"""
        if file_info.is_test:
            return "🧪"
        elif file_info.is_config:
            return "⚙️"
        elif file_info.is_documentation:
            return "📄"
        elif file_info.extension in [".py"]:
            return "🐍"
        elif file_info.extension in [".js", ".ts", ".jsx", ".tsx"]:
            return "📜"
        elif file_info.extension in [".go"]:
            return "🐹"
        elif file_info.extension in [".rs"]:
            return "🦀"
        elif file_info.extension in [".java"]:
            return "☕"
        else:
            return "📄"

    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram of project structure"""
        lines = ["```mermaid", "graph TD"]

        # Generate nodes
        node_counter = 0
        node_map = {}

        def add_node(path: str, label: str, node_type: str = "default"):
            nonlocal node_counter
            node_id = f"N{node_counter}"
            node_counter += 1
            node_map[path] = node_id

            style = {
                "root": f"{node_id}[{label}]",
                "dir": f"{node_id}[{label}]",
                "file": f"{node_id}(({label}))",
                "config": f"{node_id}{{{label}}}",
                "test": f"{node_id}[/{label}/]",
                "doc": f"{node_id}>{label}]",
            }

            lines.append(f"    {style.get(node_type, style['file'])}")
            return node_id

        # Root
        root_id = add_node("root", self.root.name, "root")

        def process_dir(dir_info: DirectoryInfo, parent_id: str, parent_path: str):
            current_path = (
                f"{parent_path}/{dir_info.path.name}"
                if parent_path
                else dir_info.path.name
            )

            if dir_info.files or dir_info.subdirs:
                dir_id = add_node(current_path, dir_info.path.name, "dir")
                lines.append(f"    {parent_id} --> {dir_id}")

                # Add files
                for file_info in dir_info.files:
                    file_path = f"{current_path}/{file_info.path.name}"

                    if file_info.is_config:
                        file_id = add_node(file_path, file_info.path.name, "config")
                    elif file_info.is_test:
                        file_id = add_node(file_path, file_info.path.name, "test")
                    elif file_info.is_documentation:
                        file_id = add_node(file_path, file_info.path.name, "doc")
                    else:
                        file_id = add_node(file_path, file_info.path.name, "file")

                    lines.append(f"    {dir_id} --> {file_id}")

                # Process subdirs
                for subdir in dir_info.subdirs:
                    process_dir(subdir, dir_id, current_path)

        for subdir in self.tree.subdirs:
            process_dir(subdir, root_id, "")

        lines.append("```")
        return "\n".join(lines)

    def generate_dependency_graph(self) -> str:
        """Generate Mermaid dependency graph"""
        lines = ["```mermaid", "graph LR"]

        # Collect all imports
        imports_map = {}
        for file_info in self._all_files():
            if file_info.imports:
                imports_map[file_info.relative_path] = file_info.imports

        # Create edges
        for file_path, imports in imports_map.items():
            file_id = file_path.replace("/", "_").replace(".", "_")
            lines.append(f"    {file_id}[{file_path}]")

            for imp in imports[:5]:  # Limit to first 5 imports
                imp_id = imp.replace("/", "_").replace(".", "_")
                lines.append(f"    {file_id} --> {imp_id}")

        lines.append("```")
        return "\n".join(lines)

    def _all_files(self) -> List[FileInfo]:
        """Get all files recursively"""
        files = []

        def collect(dir_info: DirectoryInfo):
            files.extend(dir_info.files)
            for subdir in dir_info.subdirs:
                collect(subdir)

        if self.tree:
            collect(self.tree)

        return files

    def generate_markdown(self) -> str:
        """Generate complete PROJECT_MAP.md content"""
        if not self.tree:
            self.scan_project()

        self.calculate_metrics()

        sections = [
            self._generate_header(),
            self._generate_overview(),
            self._generate_metrics(),
            self._generate_structure(),
            self._generate_mermaid_structure(),
            self._generate_architecture_diagram(),
            self._generate_dependency_graph(),
            self._generate_file_index(),
            self._generate_footer(),
        ]

        return "\n\n".join(sections)

    def _generate_header(self) -> str:
        """Generate document header"""
        return f"""# 📍 PROJECT MAP

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Version:** v2.2  
**Project:** AOKhmer  
**Auto-generated by:** `scripts/project_map_generator.py`

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Metrics](#metrics)
3. [Directory Structure](#directory-structure)
4. [Architecture Diagram](#architecture-diagram)
5. [Dependency Graph](#dependency-graph)
6. [File Index](#file-index)

---
"""

    def _generate_overview(self) -> str:
        """Generate overview section"""
        return f"""## 🎯 Overview

This document provides a comprehensive map of the AOKhmer project structure, including:

- Complete directory tree with file statistics
- Language distribution and code metrics
- Mermaid diagrams for visual navigation
- Dependency relationships between modules
- Automated updates via CI/CD pipeline

**Quick Stats:**
- Total Files: {self.metrics.get("total_files", 0):,}
- Total Lines of Code: {self.metrics.get("total_lines", 0):,}
- Languages: {len(self.metrics.get("languages", {}))}
- Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---
"""

    def _generate_metrics(self) -> str:
        """Generate metrics section"""
        lines = ["## 📊 Metrics\n"]

        # Language breakdown
        lines.append("### Language Distribution\n")
        lines.append("| Language | Files | Lines | Percentage |")
        lines.append("|----------|-------|-------|------------|")

        for lang, stats in sorted(
            self.metrics.get("languages", {}).items(),
            key=lambda x: x[1]["count"],
            reverse=True,
        )[:10]:
            lines.append(
                f"| {lang} | {stats['count']} | {stats['lines']:,} | {stats.get('percentage', 0)}% |"
            )

        # File types
        lines.append("\n### File Types\n")
        lines.append("| Type | Count | Percentage |")
        lines.append("|------|-------|------------|")

        file_types = self.metrics.get("file_types", {})
        total = self.metrics.get("total_files", 1)

        for ftype, count in file_types.items():
            pct = round(count / total * 100, 1)
            lines.append(f"| {ftype.capitalize()} | {count} | {pct}% |")

        lines.append("\n---\n")
        return "\n".join(lines)

    def _generate_structure(self) -> str:
        """Generate directory structure section"""
        return f"""## 📁 Directory Structure

```
{self.generate_text_tree(self.tree)}
```

---
"""

    def _generate_mermaid_structure(self) -> str:
        """Generate Mermaid structure diagram"""
        return f"""## 🗺️ Mermaid Structure Diagram

Interactive visualization of the project structure:

{self.generate_mermaid_diagram()}

---
"""

    def _generate_architecture_diagram(self) -> str:
        """Generate architecture overview diagram"""
        return """## 🏗️ Architecture Diagram

High-level system architecture:

```mermaid
graph TB
    subgraph Frontend["🎨 Frontend Layer"]
        A[Flutter App]
        B[Web Dashboard]
    end
    
    subgraph API["⚡ API Gateway"]
        C[FastAPI Server]
        D[WebSocket Handler]
    end
    
    subgraph Services["🔧 Services"]
        E[Dify AI Engine]
        F[n8n Workflows]
        G[Prefect Orchestration]
    end
    
    subgraph Storage["💾 Storage"]
        H[(PostgreSQL)]
        I[(ChromaDB)]
        J[(Redis)]
        K[(Elasticsearch)]
    end
    
    subgraph Monitoring["📊 Monitoring"]
        L[Prometheus]
        M[Grafana]
    end
    
    A --> C
    B --> C
    C --> E
    C --> F
    C --> G
    E --> H
    E --> I
    F --> J
    G --> H
    C --> L
    L --> M
```

---
"""

    def _generate_dependency_graph(self) -> str:
        """Generate dependency graph section"""
        return f"""## 🔗 Dependency Graph

Key module dependencies:

{self.generate_dependency_graph()}

---
"""

    def _generate_file_index(self) -> str:
        """Generate file index section"""
        lines = ["## 📑 File Index\n"]
        lines.append("Quick reference of key files:\n")

        # Group files by type
        source_files = []
        test_files = []
        config_files = []
        doc_files = []

        for file_info in self._all_files():
            if file_info.is_test:
                test_files.append(file_info)
            elif file_info.is_config:
                config_files.append(file_info)
            elif file_info.is_documentation:
                doc_files.append(file_info)
            else:
                source_files.append(file_info)

        # Config files
        if config_files:
            lines.append("### ⚙️ Configuration Files\n")
            for f in sorted(config_files, key=lambda x: x.relative_path)[:20]:
                lines.append(f"- `{f.relative_path}` - {f.line_count} lines")
            lines.append("")

        # Source files (top 20)
        if source_files:
            lines.append("### 💻 Source Files (Top 20)\n")
            for f in sorted(source_files, key=lambda x: x.line_count, reverse=True)[
                :20
            ]:
                lines.append(f"- `{f.relative_path}` - {f.line_count} lines")
            lines.append("")

        # Test files
        if test_files:
            lines.append("### 🧪 Test Files\n")
            for f in sorted(test_files, key=lambda x: x.relative_path)[:10]:
                lines.append(f"- `{f.relative_path}` - {f.line_count} lines")
            lines.append("")

        lines.append("---\n")
        return "\n".join(lines)

    def _generate_footer(self) -> str:
        """Generate document footer"""
        return f"""## 📝 Notes

- This map is auto-generated by `scripts/project_map_generator.py`
- Run `python scripts/project_map_generator.py --watch` to auto-update on file changes
- For manual updates, edit the generator script directly

---

**End of Project Map** | Last Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    def save(self, output_path: Optional[str] = None):
        """Save the generated map to file"""
        path = Path(output_path) if output_path else self.output_path
        content = self.generate_markdown()

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Project map saved to: {path}")
        return path

    def watch(self):
        """Watch for file changes and auto-regenerate"""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler

            class ProjectChangeHandler(FileSystemEventHandler):
                def __init__(self, generator):
                    self.generator = generator
                    self.last_update = 0

                def on_any_event(self, event):
                    import time

                    current_time = time.time()
                    # Debounce: only update every 5 seconds
                    if current_time - self.last_update > 5:
                        if not event.src_path.endswith("PROJECT_MAP.md"):
                            print(f"🔄 Change detected: {event.src_path}")
                            self.generator.scan_project()
                            self.generator.save()
                            self.last_update = current_time

            print("👀 Watching for changes... (Press Ctrl+C to stop)")
            observer = Observer()
            observer.schedule(ProjectChangeHandler(self), self.root, recursive=True)
            observer.start()

            try:
                while True:
                    import time

                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("\n👋 Stopped watching")

            observer.join()

        except ImportError:
            print("⚠️  watchdog not installed. Install with: pip install watchdog")
            print("   Falling back to one-time generation...")
            self.save()


def main():
    parser = argparse.ArgumentParser(
        description="Generate PROJECT_MAP.md with project structure and diagrams"
    )
    parser.add_argument(
        "--root",
        "-r",
        default=".",
        help="Root directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="PROJECT_MAP.md",
        help="Output file path (default: PROJECT_MAP.md)",
    )
    parser.add_argument(
        "--watch",
        "-w",
        action="store_true",
        help="Watch for changes and auto-regenerate",
    )
    parser.add_argument(
        "--metrics-only",
        "-m",
        action="store_true",
        help="Only output metrics (no full map)",
    )

    args = parser.parse_args()

    generator = ProjectMapGenerator(args.root, args.output)

    if args.metrics_only:
        metrics = generator.calculate_metrics()
        print(json.dumps(metrics, indent=2))
    elif args.watch:
        generator.watch()
    else:
        generator.scan_project()
        generator.save()


if __name__ == "__main__":
    main()
