"""AI-powered description enrichment for macros."""

import json
import sqlite3
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Optional

from .utils import module_hint


class AIEnricher:
    """Enriches macro descriptions using Azure OpenAI."""

    SYSTEM_PROMPT = """
You are documenting MicroPython build-time macros. Stay within provided context.
avoid vague phrases like "used to", "This defines" or "specifies" and avoid overly use in "in MicroPython" as that is quite clear.
If the purpose is unclear, respond with "unknown". Output a concise description in one line. 
If possible add a few examples on a 2nd line.
""".strip()

    GROUP_SUMMARY_PROMPT = """
You are documenting a group of related MicroPython build-time macros.
Given a list of macros with their names and descriptions, write a concise 2-3 sentence summary 
that explains what this group of macros controls or configures.
Focus on the common theme and practical purpose.
Do not list individual macros. Do not use phrases like "This group" or "These macros" or "in MicroPython".
Return JSON: {"summary": "..."}
""".strip()

    def __init__(
        self,
        root: Path,
        db_path: Path,
        cache_path: Optional[Path] = None,
        batch_size: int = 20,
        occurrence_limit: int = 20,
        occurrence_radius: int = 5,
        temperature: float = 0.01,
    ):
        """
        Initialize the AI enricher.

        Args:
            root: Root directory of the MicroPython repository
            db_path: Path to the SQLite database
            cache_path: Path for disk cache (defaults to db_path parent / ai_cache)
            batch_size: Number of parallel API calls per batch
            occurrence_limit: Max occurrences to include in context
            occurrence_radius: Lines of context around each occurrence
            temperature: LLM temperature setting
        """
        self.root = root.resolve()
        self.db_path = db_path
        self.cache_path = cache_path or (db_path.parent / "ai_cache")
        self.batch_size = batch_size
        self.occurrence_limit = occurrence_limit
        self.occurrence_radius = occurrence_radius
        self.temperature = temperature

        self._cache = None
        self._client = None
        self._deployment = None
        self.conn: Optional[sqlite3.Connection] = None
        self.cur: Optional[sqlite3.Cursor] = None

    def _get_cache(self):
        """Lazily initialize disk cache."""
        if self._cache is None:
            from diskcache import Cache

            self._cache = Cache(str(self.cache_path))
        return self._cache

    def _get_client(self):
        """Lazily get the Azure OpenAI client."""
        if self._client is None:
            from .ai_client import get_client, get_deployment

            self._client = get_client()
            self._deployment = get_deployment()
        return self._client

    def _ensure_db(self) -> None:
        """Ensure database connection is open."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cur = self.conn.cursor()

    def _get_candidates(self) -> List[tuple]:
        """Get macros with missing descriptions."""
        self._ensure_db()
        assert self.cur is not None
        return self.cur.execute(
            """
            SELECT m.name, m.value, COALESCE(m.description, m.comment, '') as description, 
                   m.comment, m.file, m.line
            FROM macros m
            WHERE (m.description_ai IS NULL OR length(m.description_ai)=0)
            """
        ).fetchall()

    def _top_modules(self, name: str, limit: int = 3) -> str:
        """Get top modules where a macro is used."""
        assert self.cur is not None
        rows = self.cur.execute("SELECT file FROM occurrences WHERE name=?", (name,)).fetchall()
        counter = Counter(module_hint(r[0]) for r in rows)
        return ", ".join(f"{m} ({c})" for m, c in counter.most_common(limit))

    def _get_occurrence_contexts(self, name: str) -> str:
        """Get code context around macro occurrences."""
        assert self.cur is not None
        rows = self.cur.execute(
            "SELECT file, line FROM occurrences WHERE name=? LIMIT ?",
            (name, self.occurrence_limit),
        ).fetchall()

        blocks = []
        for file, line in rows:
            path = self.root / file
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
                lines = text.splitlines()
                start = max(0, line - 1 - self.occurrence_radius)
                end = min(len(lines), line + self.occurrence_radius)
                snippet_lines = [f"{idx + 1}: {lines[idx]}" for idx in range(start, end)]
                blocks.append(f"{file}:{line}\n" + "\n".join(snippet_lines))
            except Exception:
                continue
        return "\n\n".join(blocks)

    def _build_user_prompt(self, rec: Dict[str, Any]) -> str:
        """Build the user prompt for a single macro."""
        return dedent(f"""
        Macro: {rec["name"]}
        Value: {rec.get("value") or ""}
        Existing description/comment: {rec.get("description") or rec.get("comment") or ""}
        Location: {rec["file"]}:{rec["line"]}
        Top modules: {rec.get("modules", "")}
        Occurrences (±{self.occurrence_radius} lines):
        {rec.get("occurrences", "")}
        Task: One-line purpose; if unclear, reply "unknown".
        Return JSON: {{"name": "{rec["name"]}", "description": "..."}}
        """)

    def _make_cache_key(self, rec: Dict[str, Any]) -> str:
        """Generate a cache key for a macro record."""
        parts = [
            rec.get("name", ""),
            rec.get("value", ""),
            rec.get("description", ""),
            rec.get("comment", ""),
            rec.get("occurrences", ""),
        ]
        raw = "\u0001".join(parts)
        return sha256(raw.encode("utf-8")).hexdigest()

    def _call_azure_one(self, rec: Dict[str, Any]) -> str:
        """Call Azure OpenAI for a single macro description."""
        cache = self._get_cache()
        cache_key = self._make_cache_key(rec)
        cached = cache.get(cache_key)
        if cached is not None:
            return str(cached)

        client = self._get_client()
        assert self._deployment is not None
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": self._build_user_prompt(rec)},
        ]

        try:
            resp = client.chat.completions.create(
                model=self._deployment,
                # store=True, # 
                messages=messages,  # type: ignore[arg-type]
                temperature=self.temperature,
                max_tokens=256,
                response_format={"type": "json_object"},
            )
            content = resp.choices[0].message.content
            try:
                data = json.loads(content or "{}")
                desc = (data.get("description") or "").strip()
            except Exception:
                desc = ""
        except Exception as e:
            print(f"\nError communicating with Azure OpenAI: {e}")
            desc = ""

        if desc:
            cache.set(cache_key, desc)
        return desc

    def generate_missing_descriptions(self, verbose: bool = True) -> int:
        """
        Generate descriptions for macros with missing descriptions.

        Returns:
            Number of macros updated
        """
        self._ensure_db()
        candidates = self._get_candidates()
        total = len(candidates)

        if verbose:
            print(f"Processing {total} candidates in batches of {self.batch_size}")

        updated = 0
        processed = 0

        def build_macro_info(row):
            name, value, description, comment, file, line = row
            return {
                "name": name,
                "value": value,
                "description": description,
                "comment": comment,
                "file": file,
                "line": line,
                "modules": self._top_modules(name, limit=3),
                "occurrences": self._get_occurrence_contexts(name),
            }

        for batch_start in range(0, total, self.batch_size):
            batch_end = min(batch_start + self.batch_size, total)
            batch = candidates[batch_start:batch_end]
            macro_infos = [build_macro_info(row) for row in batch]

            results = []
            with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
                future_to_idx = {
                    executor.submit(self._call_azure_one, info): idx
                    for idx, info in enumerate(macro_infos)
                }
                for future in as_completed(future_to_idx):
                    idx = future_to_idx[future]
                    try:
                        results.append((idx, future.result()))
                    except Exception as e:
                        if verbose:
                            print(f"\nError processing {macro_infos[idx]['name']}: {e}")
                        results.append((idx, ""))

            results.sort(key=lambda x: x[0])
            for idx, description_ai in results:
                if description_ai and description_ai.lower() != "unknown":
                    assert self.cur is not None and self.conn is not None
                    self.cur.execute(
                        "UPDATE macros SET description_ai=?, description=? WHERE name=?",
                        (description_ai, description_ai, macro_infos[idx]["name"]),
                    )
                    self.conn.commit()
                    updated += 1

            processed += len(batch)
            if verbose:
                print(
                    f"Batch {batch_start // self.batch_size + 1}: "
                    f"{processed}/{total} processed, {updated} updated",
                    flush=True,
                )

        if verbose:
            print(f"\nCompleted: {updated}/{total} descriptions updated")
        return updated

    def _build_group_summary_prompt(self, group_name: str, items: List[Dict[str, Any]]) -> str:
        """Build prompt for group summary."""
        from .utils import sanitize_for_markdown

        macro_list = "\n".join(
            f"- {item['name']}: {sanitize_for_markdown(item.get('description', '') or '')[:200]}"
            for item in items[:30]
        )
        return f"""
Group: {group_name}
Number of macros: {len(items)}

Macros in this group:
{macro_list}

Write a 2-3 sentence summary of what this group configures.
Return JSON: {{"summary": "..."}}
"""

    def _call_azure_group_summary(self, group_name: str, items: List[Dict[str, Any]]) -> str:
        """Generate a summary for a group of macros."""
        cache = self._get_cache()
        item_names = sorted(item["name"] for item in items)
        cache_key = sha256(f"group:{group_name}:{','.join(item_names)}".encode()).hexdigest()

        cached = cache.get(cache_key)
        if cached is not None:
            return str(cached)

        client = self._get_client()
        assert self._deployment is not None
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.GROUP_SUMMARY_PROMPT},
            {"role": "user", "content": self._build_group_summary_prompt(group_name, items)},
        ]

        try:
            resp = client.chat.completions.create(
                model=self._deployment,
                messages=messages,  # type: ignore[arg-type]
                temperature=self.temperature,
                max_tokens=256,
                response_format={"type": "json_object"},
            )
            content = resp.choices[0].message.content
            if content is None:
                summary = ""
            else:
                data = json.loads(content)
                summary = (data.get("summary") or "").strip()
        except Exception as e:
            print(f"\nError generating group summary for {group_name}: {e}")
            summary = ""

        if summary:
            cache.set(cache_key, summary)
        return summary

    def generate_group_summaries(
        self,
        groups: Dict[str, List[Dict[str, Any]]],
        min_items: int = 3,
        verbose: bool = True,
    ) -> Dict[str, str]:
        """Generate summaries for groups with min_items or more items."""
        groups_to_summarize = {
            name: items for name, items in groups.items() if len(items) >= min_items
        }

        if not groups_to_summarize:
            return {}

        if verbose:
            print(f"Generating summaries for {len(groups_to_summarize)} groups...")

        summaries = {}
        group_list = list(groups_to_summarize.items())

        for batch_start in range(0, len(group_list), self.batch_size):
            batch = group_list[batch_start : batch_start + self.batch_size]

            with ThreadPoolExecutor(max_workers=self.batch_size) as executor:
                future_to_name = {
                    executor.submit(self._call_azure_group_summary, name, items): name
                    for name, items in batch
                }
                for future in as_completed(future_to_name):
                    name = future_to_name[future]
                    try:
                        summaries[name] = future.result()
                    except Exception as e:
                        if verbose:
                            print(f"\nError processing group {name}: {e}")
                        summaries[name] = ""

            if verbose:
                print(
                    f"  Batch {batch_start // self.batch_size + 1}: "
                    f"{min(batch_start + self.batch_size, len(group_list))}/{len(group_list)}",
                    flush=True,
                )

        return summaries

    def close(self) -> None:
        """Close database connection and cache."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cur = None
        if self._cache:
            self._cache.close()
            self._cache = None
