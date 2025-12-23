"""Scanner for MICROPY_* and MP_* macros in the MicroPython codebase."""

import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Optional, Pattern, Set

from .utils import choose_best_description, macro_category, module_hint


class MacroScanner:
    """Scans codebase for macros with configurable prefix and stores results in SQLite."""

    IGNORE_PARTS: Set[str] = {
        "emsdk",
        "esp-idf",
        ".git",
        ".venv",
        "build",
        "htmlcov",
        "docs",
        "pico-sdk",
        "multipage_pair_report",
        "obj_compare_out",
        "binary_compare_out",
        "myenv",
        "__pycache__",
        "scratch",
    }

    ALLOWED_NAMES: Set[str] = {"Makefile", "CMakeLists.txt"}

    ALLOWED_SUFFIXES: Set[str] = {
        ".c",
        ".h",
        ".cpp",
        ".hpp",
        ".mk",
        ".cmake",
        ".ld",
        ".py",
        ".rst",
        ".md",
        ".inc",
        ".S",
        ".s",
        ".txt",
    }

    # Filename patterns to exclude (generated output files)
    IGNORE_PATTERNS: Set[str] = {
        "macros_",  # Excludes macros_*.md and macros_*.rst
    }

    # Default location for database (module's parent folder)
    DEFAULT_DB_DIR = Path(__file__).parent.parent
    DEFAULT_DB_NAME = "macros.db"
    
    # Preset configurations for different macro prefixes
    PRESETS = {
        "MICROPY": {
            "prefix": "MICROPY_",
            "db_name": "macros.db",
            "output_name": "macros.md",
        },
        "MP": {
            "prefix": "MP_",
            "db_name": "mp_macros.db",
            "output_name": "mp_macros.md",
        },
    }

    def __init__(
        self,
        root: Path,
        db_path: Optional[Path] = None,
        prefix: str = "MICROPY_",
    ):
        """
        Initialize the scanner.

        Args:
            root: Root directory of the MicroPython repository
            db_path: Path to SQLite database (defaults to tools/document_gen/macros.db)
            prefix: Macro prefix to scan for (e.g., 'MICROPY_' or 'MP_')
        """
        self.root = root.resolve()
        self.prefix = prefix
        self.db_path = db_path or (self.DEFAULT_DB_DIR / self.DEFAULT_DB_NAME)
        self.conn: Optional[sqlite3.Connection] = None
        self.cur: Optional[sqlite3.Cursor] = None
        
        # Build regex patterns based on prefix
        self._define_re: Pattern[str] = re.compile(
            rf"^\s*#\s*define\s+({re.escape(prefix)}[A-Z0-9_]+)(?:\s+(.*))?$"
        )
        self._macro_use_re: Pattern[str] = re.compile(
            rf"{re.escape(prefix)}[A-Z0-9_]+"
        )

    def _is_code_file(self, path: Path) -> bool:
        """Check if a path should be scanned."""
        if path.is_dir():
            return False
        if any(part in self.IGNORE_PARTS for part in path.parts):
            return False
        # Exclude generated output files (macros_*.md, macros_*.rst)
        if any(path.name.startswith(pattern) for pattern in self.IGNORE_PATTERNS):
            return False
        if path.name in self.ALLOWED_NAMES:
            return True
        return path.suffix in self.ALLOWED_SUFFIXES

    def _get_code_files(self) -> List[Path]:
        """Get all code files in the repository."""
        return [p for p in self.root.rglob("*") if self._is_code_file(p)]

    def _init_db(self) -> None:
        """Initialize the database connection and ensure schema exists."""
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
        # Create tables if they don't exist (preserves existing data)
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS macros (
                name TEXT PRIMARY KEY,
                file TEXT,
                line INTEGER,
                value TEXT,
                comment TEXT,
                description TEXT,
                kind TEXT,
                description_ai TEXT
            );

            CREATE TABLE IF NOT EXISTS occurrences (
                name TEXT,
                file TEXT,
                line INTEGER,
                snippet TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_occurrences_name ON occurrences(name);
        """)
        self.conn.commit()

    def _clear_prefix_data(self) -> None:
        """Remove all data for the current prefix before re-scanning."""
        assert self.cur is not None and self.conn is not None
        # Delete macros matching this prefix
        self.cur.execute("DELETE FROM macros WHERE name LIKE ?", (f"{self.prefix}%",))
        # Delete occurrences matching this prefix
        self.cur.execute("DELETE FROM occurrences WHERE name LIKE ?", (f"{self.prefix}%",))
        self.conn.commit()

    def _extract_leading_comment(self, lines: List[str], idx: int) -> str:
        """Extract comment lines preceding a #define."""
        comment_lines = []
        j = idx - 2  # zero-based index for list
        while j >= 0:
            stripped = lines[j].strip()
            if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
                comment_lines.insert(0, stripped.strip("/ *"))
                j -= 1
                continue
            break
        return " ".join(comment_lines)

    def _better_def(self, existing: Optional[dict], candidate: dict) -> dict:
        """Choose the better definition (longer comment or value)."""
        if existing is None:
            return candidate
        if len(candidate["comment"]) > len(existing["comment"]):
            return candidate
        if len(candidate["comment"]) == len(existing["comment"]) and len(candidate["value"]) > len(
            existing["value"]
        ):
            return candidate
        return existing

    def _collect_definitions(self, code_files: List[Path]) -> int:
        """Collect macro definitions from all code files."""
        best_by_name = {}

        for path in code_files:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = text.splitlines()
            for idx, line in enumerate(lines, start=1):
                m = self._define_re.match(line)
                if not m:
                    continue

                name = m.group(1)
                value = (m.group(2) or "").strip()
                comment = self._extract_leading_comment(lines, idx)

                rec = {
                    "name": name,
                    "value": value,
                    "comment": comment,
                    "description": comment,
                    "file": path.relative_to(self.root).as_posix(),
                    "line": idx,
                    "kind": "define",
                    "description_ai": None,
                }
                best_by_name[name] = self._better_def(best_by_name.get(name), rec)

        rows = [
            (
                r["name"],
                r["file"],
                r["line"],
                r["value"],
                r["comment"],
                r["description"],
                r["kind"],
                r["description_ai"],
            )
            for r in best_by_name.values()
        ]

        assert self.cur is not None
        self.cur.executemany(
            """INSERT OR REPLACE INTO macros
               (name, file, line, value, comment, description, kind, description_ai)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            rows,
        )
        assert self.conn is not None
        self.conn.commit()
        return len(rows)

    def _collect_occurrences(self, code_files: List[Path]) -> int:
        """Collect all macro usages from code files."""
        rows = []

        for path in code_files:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            lines = text.splitlines()
            for idx, line in enumerate(lines, start=1):
                matches = self._macro_use_re.findall(line)
                if not matches:
                    continue
                snippet = line.strip()[:240]
                rows.extend(
                    (name, str(path.relative_to(self.root)), idx, snippet) for name in matches
                )

        assert self.cur is not None
        self.cur.executemany(
            "INSERT INTO occurrences (name, file, line, snippet) VALUES (?, ?, ?, ?)",
            rows,
        )
        assert self.conn is not None
        self.conn.commit()
        return len(rows)

    def scan(self, verbose: bool = True) -> tuple[int, int]:
        """
        Scan the codebase and populate the database.

        Returns:
            Tuple of (definitions_count, occurrences_count)
        """
        if verbose:
            print(f"Scanning {self.root} for {self.prefix}* macros...")

        code_files = self._get_code_files()
        if verbose:
            print(f"Found {len(code_files)} code files")

        self._init_db()
        self._clear_prefix_data()

        def_count = self._collect_definitions(code_files)
        if verbose:
            print(f"Collected {def_count} macro definitions")

        occ_count = self._collect_occurrences(code_files)
        if verbose:
            print(f"Collected {occ_count} macro occurrences")

        return def_count, occ_count

    def build_summary(self, limit_modules: int = 5) -> List[dict]:
        """Build a summary of all macros with their metadata."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()

        assert self.cur is not None
        defs = self.cur.execute(
            "SELECT name, value, comment, description, file, line FROM macros WHERE name LIKE ?",
            (f"{self.prefix}%",),
        ).fetchall()
        occ = self.cur.execute(
            "SELECT name, file, line FROM occurrences WHERE name LIKE ?",
            (f"{self.prefix}%",),
        ).fetchall()

        mod_counts = defaultdict(Counter)
        files_per_macro = defaultdict(set)
        for name, file, line in occ:
            mod_counts[name][module_hint(file)] += 1
            files_per_macro[name].add(file)

        defs_by_name = defaultdict(list)
        for name, value, comment, description, file, line in defs:
            defs_by_name[name].append(
                {
                    "value": value,
                    "comment": comment,
                    "description": description,
                    "file": file,
                    "line": line,
                }
            )

        summary = []
        for name in sorted(defs_by_name.keys()):
            best_desc, best_loc = choose_best_description(defs_by_name[name])
            modules = ", ".join(
                f"{mod} ({count})" for mod, count in mod_counts[name].most_common(limit_modules)
            )
            summary.append(
                {
                    "name": name,
                    "category": macro_category(name, self.prefix),
                    "description": best_desc.strip(),
                    "value": defs_by_name[name][0].get("value", ""),
                    "modules": modules,
                    "definition": best_loc,
                    "files_touched": len(files_per_macro.get(name, [])),
                }
            )
        return summary

    def build_summary_with_ai(self, limit_modules: int = 5) -> List[dict]:
        """Build summary including AI-generated descriptions."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()

        assert self.cur is not None
        defs = self.cur.execute(
            "SELECT name, value, comment, description, description_ai, file, line FROM macros WHERE name LIKE ?",
            (f"{self.prefix}%",),
        ).fetchall()
        occ = self.cur.execute(
            "SELECT name, file, line FROM occurrences WHERE name LIKE ?",
            (f"{self.prefix}%",),
        ).fetchall()

        mod_counts = defaultdict(Counter)
        files_per_macro = defaultdict(set)
        for name, file, line in occ:
            mod_counts[name][module_hint(file)] += 1
            files_per_macro[name].add(file)

        defs_by_name = defaultdict(list)
        for name, value, comment, description, description_ai, file, line in defs:
            defs_by_name[name].append(
                {
                    "value": value,
                    "comment": comment,
                    "description": description,
                    "description_ai": description_ai,
                    "file": file,
                    "line": line,
                }
            )

        summary = []
        for name in sorted(defs_by_name.keys()):
            modules = ", ".join(
                f"{mod} ({count})" for mod, count in mod_counts[name].most_common(limit_modules)
            )
            best_loc = f"{defs_by_name[name][0]['file']}:{defs_by_name[name][0]['line']}"
            summary.append(
                {
                    "name": name,
                    "category": macro_category(name, self.prefix),
                    "description": (
                        defs_by_name[name][0].get("description")
                        or defs_by_name[name][0].get("description_ai")
                        or ""
                    ),
                    "value": defs_by_name[name][0].get("value", ""),
                    "modules": modules,
                    "definition": best_loc,
                    "files_touched": len(files_per_macro.get(name, [])),
                }
            )
        return summary

    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cur = None
