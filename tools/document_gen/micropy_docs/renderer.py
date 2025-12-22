"""Markdown renderer for macro documentation."""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from .utils import code_search_md, extract_second_level, sanitize_for_markdown


class MarkdownRenderer:
    """Renders macro documentation as markdown."""

    def __init__(
        self,
        output_path: Path,
        min_group_size: int = 10,
        min_summary_items: int = 2,
        subgrouped_categories: Optional[set] = None,
    ):
        """
        Initialize the renderer.

        Args:
            output_path: Path for the output markdown file
            min_group_size: Minimum items for a category to get its own section
            min_summary_items: Minimum items for a group to get an AI summary
            subgrouped_categories: Categories that should have 2nd-level subgrouping
        """
        self.output_path = output_path
        self.min_group_size = min_group_size
        self.min_summary_items = min_summary_items
        self.subgrouped_categories = subgrouped_categories or {"HW", "PY"}

    def _get_table_header(self) -> str:
        """Get the markdown table header."""
        return (
            "| Macro | Description | Sample value(s) |\n|------|-------------|-----------------|\n"
        )

    def _render_row(self, item: dict) -> str:
        """Render a single table row."""
        desc = sanitize_for_markdown(item["description"])
        val = sanitize_for_markdown(item["value"]) or "-"
        return (
            f"| {code_search_md(item['name'])} | "
            f"{desc.replace('|', '\\|').strip()} | "
            f"{val.replace('|', '\\|').strip()} |"
        )

    def render(
        self,
        summary: List[dict],
        group_summaries: Optional[Dict[str, str]] = None,
    ) -> Path:
        """
        Render the macro summary to markdown.

        Args:
            summary: List of macro summary dicts
            group_summaries: Optional dict of group name -> summary text

        Returns:
            Path to the generated markdown file
        """
        group_summaries = group_summaries or {}
        header = self._get_table_header()

        # Group by category
        grouped = defaultdict(list)
        for item in summary:
            grouped[item["category"]].append(item)

        # Filter small groups into MISC
        misc_bucket = []
        filtered = {}
        for category, items in grouped.items():
            if len(items) < self.min_group_size:
                misc_bucket.extend(items)
            else:
                filtered[category] = items
        if misc_bucket:
            filtered["MISC"] = filtered.get("MISC", []) + misc_bucket

        sections = []

        # Sort categories but ensure MISC comes last
        sorted_categories = sorted(k for k in filtered.keys() if k != "MISC")
        if "MISC" in filtered:
            sorted_categories.append("MISC")

        for category in sorted_categories:
            if category in {"INCLUDED"}:
                continue

            items = filtered[category]
            category_prefix = f"MICROPY_{category}"

            if category in self.subgrouped_categories:
                sections.append(
                    self._render_subgrouped_category(
                        category, items, category_prefix, header, group_summaries
                    )
                )
            else:
                sections.append(
                    self._render_simple_category(items, category_prefix, header, group_summaries)
                )

        md = "\n".join(sections)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(md, encoding="utf-8")
        return self.output_path

    def _render_subgrouped_category(
        self,
        category: str,
        items: List[dict],
        category_prefix: str,
        header: str,
        group_summaries: Dict[str, str],
    ) -> str:
        """Render a category with second-level subgrouping."""
        # Group by second level
        subgroups = defaultdict(list)
        for item in items:
            second_level = extract_second_level(item["name"], category)
            subgroups[second_level].append(item)

        # Separate named subgroups from general bucket
        final_subgroups = {}
        general_bucket = []
        for subcat, subitems in subgroups.items():
            if not subcat:
                general_bucket.extend(subitems)
            else:
                final_subgroups[subcat] = subitems

        # L1 section with summary
        l1_summary = group_summaries.get(category_prefix, "")
        if l1_summary:
            section_parts = [f"\n\n### {category_prefix}\n\n{l1_summary}\n"]
        else:
            section_parts = [f"\n\n### {category_prefix}\n"]

        # Render each subgroup
        for subcat in sorted(final_subgroups.keys()):
            subitems = final_subgroups[subcat]
            subgroup_prefix = f"{category_prefix}_{subcat}"
            l2_summary = group_summaries.get(subgroup_prefix, "")

            rows = [self._render_row(item) for item in sorted(subitems, key=lambda x: x["name"])]

            if l2_summary:
                section_parts.append(
                    f"\n#### {subgroup_prefix}\n\n{l2_summary}\n\n{header}" + "\n".join(rows)
                )
            else:
                section_parts.append(f"\n#### {subgroup_prefix}\n\n{header}" + "\n".join(rows))

        # Render general/misc items
        if general_bucket:
            rows = [
                self._render_row(item) for item in sorted(general_bucket, key=lambda x: x["name"])
            ]
            section_parts.append(f"\n#### {category_prefix} (other)\n\n{header}" + "\n".join(rows))

        return "".join(section_parts)

    def _render_simple_category(
        self,
        items: List[dict],
        category_prefix: str,
        header: str,
        group_summaries: Dict[str, str],
    ) -> str:
        """Render a simple single-level category."""
        l1_summary = group_summaries.get(category_prefix, "")
        rows = [self._render_row(item) for item in sorted(items, key=lambda x: x["name"])]
        section_md = header + "\n".join(rows)

        if l1_summary:
            return f"\n\n### {category_prefix}\n\n{l1_summary}\n\n" + section_md
        else:
            return f"\n\n### {category_prefix}\n\n" + section_md

    def collect_groups_for_summaries(self, summary: List[dict]) -> Dict[str, List[dict]]:
        """
        Collect all groups (L1 and L2) for summary generation.

        Returns:
            Dict mapping group prefix to list of items
        """
        grouped = defaultdict(list)
        for item in summary:
            grouped[item["category"]].append(item)

        # Filter small groups into MISC
        misc_bucket = []
        filtered = {}
        for category, items in grouped.items():
            if len(items) < self.min_group_size:
                misc_bucket.extend(items)
            else:
                filtered[category] = items
        if misc_bucket:
            filtered["MISC"] = filtered.get("MISC", []) + misc_bucket

        all_groups = {}

        for category in filtered.keys():
            if category in {"INCLUDED"}:
                continue

            items = filtered[category]
            category_prefix = f"MICROPY_{category}"

            if category in self.subgrouped_categories:
                all_groups[category_prefix] = items

                # Add L2 subgroups
                subgroups = defaultdict(list)
                for item in items:
                    second_level = extract_second_level(item["name"], category)
                    if second_level:
                        subgroups[second_level].append(item)

                for subcat, subitems in subgroups.items():
                    subgroup_prefix = f"{category_prefix}_{subcat}"
                    all_groups[subgroup_prefix] = subitems
            else:
                all_groups[category_prefix] = items

        return all_groups
