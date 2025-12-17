from pathlib import Path
import re
import sqlite3
from textwrap import dedent
import os
from typing import List, Dict, Any
from az_102 import client , DEPLOYMENT
from macro_utils import module_hint, macro_category

ROOT = Path('D:\\mypython\\micropython').resolve()
DB_PATH = ROOT / 'scratch' / 'micropy_macros.db'
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()



# Fetch candidates with empty/short descriptions
MIN_LEN = 15
candidates = cur.execute(
    """
    SELECT m.name, m.value, COALESCE(m.description, m.comment, '') as description, m.comment, m.file, m.line
    FROM macros m
    WHERE (m.description_ai IS NULL OR length(m.description_ai)=0)
      AND (m.description IS NULL OR length(m.description) < ?)
    LIMIT 2000
    """,
    (MIN_LEN,),
).fetchall()
len(candidates)



SYSTEM_PROMPT = """
You are documenting MicroPython build-time macros. Stay within provided context.
If the purpose is unclear, respond with "unknown". Output a concise discription of one or two lines.
""".strip()


import json
from collections import Counter, defaultdict
from hashlib import sha256

from azure.identity import DefaultAzureCredential  # optional; only needed for AAD/managed identity
from diskcache import Cache

TIMEOUT = 60

OCCURRENCE_LIMIT = 8
OCCURRENCE_RADIUS = 3
AI_TEMPERATURE = 0.01

CACHE_PATH = ROOT / 'scratch' / 'ai_cache'
cache = Cache(str(CACHE_PATH))


def top_modules(name: str, limit: int = 3) -> str:
    rows = cur.execute("SELECT file FROM occurrences WHERE name=?", (name,)).fetchall()
    counter = Counter(module_hint(r[0]) for r in rows)
    return ', '.join(f"{m} ({c})" for m, c in counter.most_common(limit))


def get_occurrence_contexts(name: str, radius: int = OCCURRENCE_RADIUS, limit: int = OCCURRENCE_LIMIT) -> str:
    rows = cur.execute(
        "SELECT file, line FROM occurrences WHERE name=? LIMIT ?",
        (name, limit),
    ).fetchall()
    blocks = []
    for file, line in rows:
        path = ROOT / file
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
            lines = text.splitlines()
            start = max(0, line - 1 - radius)
            end = min(len(lines), line + radius)
            snippet_lines = []
            for idx in range(start, end):
                snippet_lines.append(f"{idx + 1}: {lines[idx]}")
            blocks.append(f"{file}:{line}\n" + "\n".join(snippet_lines))
        except Exception:
            continue
    return "\n\n".join(blocks)


def build_user_prompt(rec: Dict[str, Any]) -> str:
    name = rec['name']
    value = rec.get('value') or ''
    description = rec.get('description') or ''
    comment = rec.get('comment') or ''
    loc = f"{rec['file']}:{rec['line']}"
    modules = rec.get('modules', '')
    occurrences = rec.get('occurrences', '')
    return dedent(f"""
    Macro: {name}
    Value: {value}
    Existing description/comment: {description or comment}
    Location: {loc}
    Top modules: {modules}
    Occurrences (±{OCCURRENCE_RADIUS} lines):
    {occurrences}
    Task: One-line purpose; if unclear, reply "unknown".
    Return JSON: {{"name": "{name}", "description": "..."}}
    """)


def make_cache_key(rec: Dict[str, Any]) -> str:
    parts = [
        rec.get('name', ''),
        rec.get('value', ''),
        rec.get('description', ''),
        rec.get('comment', ''),
        rec.get('occurrences', ''),
    ]
    raw = "\u0001".join(parts)
    return sha256(raw.encode('utf-8')).hexdigest()


# Build enriched candidate records
cand_rows: List[Dict[str, Any]] = []
for name, value, description, comment, file, line in candidates:
    cand_rows.append(
        {
            'name': name,
            'value': value,
            'description': description,
            'comment': comment,
            'file': file,
            'line': line,
            'modules': top_modules(name, limit=3),
            'occurrences': get_occurrence_contexts(name),
        }
    )

print(f"Candidates needing AI description: {len(cand_rows)}")




def call_azure_one(rec: Dict[str, Any]) -> str:
    cache_key = make_cache_key(rec)
    cached = cache.get(cache_key)
    if cached is not None:
        return str(cached)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(rec)},
    ]

    try:
        resp = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=messages,
            temperature=AI_TEMPERATURE,
            max_tokens=256,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        try:
            data = json.loads(content)
            desc = (data.get("description") or '').strip()
        except Exception:
            desc = ''
    except Exception as e:
        print(f"\nError communicating with Azure OpenAI: {e}")
        desc = ''

    cache.set(cache_key, desc)
    return desc


updated = 0
progress_bar = ''
if cand_rows:
    total = len(cand_rows)
    for idx, rec in enumerate(cand_rows, start=1):
        try:
            desc = call_azure_one(rec)
        except Exception as e:
            print(f"\nError processing {rec['name']}: {e}")
            continue
        if desc and desc.lower() != 'unknown':
            cur.execute(
                "UPDATE macros SET description_ai=?, description=? WHERE name=?",
                (desc, desc, rec['name']),
            )
            conn.commit()
            updated += 1
        progress_bar += '>'
        print(f"{progress_bar} {idx}/{total}", end='\r', flush=True)
        if len(progress_bar) > 50:
            progress_bar = ""
            print("\n")
    print(f"\nAI descriptions updated: {updated}/{total}")




# Regenerate summary/markdown preferring description_ai when available

def choose_best_description(defs_for_name):
    ai = [d for d in defs_for_name if d.get('description_ai')]
    if ai:
        ai.sort(key=lambda d: len(d['description_ai']), reverse=True)
        return ai[0]['description_ai']
    descr = [d for d in defs_for_name if d.get('description')]
    if descr:
        descr.sort(key=lambda d: len(d['description']), reverse=True)
        return descr[0]['description']
    comment_candidates = [d for d in defs_for_name if d.get('comment')]
    if comment_candidates:
        comment_candidates.sort(key=lambda d: len(d['comment']), reverse=True)
        return comment_candidates[0]['comment']
    value_candidates = [d for d in defs_for_name if d.get('value')]
    if value_candidates:
        value_candidates.sort(key=lambda d: len(d['value']), reverse=True)
        return value_candidates[0]['value']
    return ''


def build_summary_with_ai(limit_modules: int = 5):
    defs = cur.execute(
        "SELECT name, value, comment, description, description_ai, file, line FROM macros"
    ).fetchall()
    occ = cur.execute(
        "SELECT name, file, line FROM occurrences"
    ).fetchall()

    mod_counts = defaultdict(Counter)
    files_per_macro = defaultdict(set)
    for name, file, line in occ:
        mod_counts[name][module_hint(file)] += 1
        files_per_macro[name].add(file)

    defs_by_name = defaultdict(list)
    for name, value, comment, description, description_ai, file, line in defs:
        defs_by_name[name].append({
            'value': value,
            'comment': comment,
            'description': description,
            'description_ai': description_ai,
            'file': file,
            'line': line,
        })

    summary = []
    for name in sorted(defs_by_name.keys()):
        best_desc = (choose_best_description(defs_by_name[name]) or '').strip()
        modules = ', '.join(
            f"{mod} ({count})" for mod, count in mod_counts[name].most_common(limit_modules)
        )
        best_loc = f"{defs_by_name[name][0]['file']}:{defs_by_name[name][0]['line']}"
        summary.append(
            {
                'name': name,
                'category': macro_category(name),
                'description': best_desc,
                'value': defs_by_name[name][0].get('value', ''),
                'modules': modules,
                'definition': best_loc,
                'files_touched': len(files_per_macro.get(name, [])),
            }
        )
    return summary


def render_markdown_with_ai(summary, min_group_size: int = 11):
    header = "| Macro | Description | Value | Top Modules (uses) | Defined at |\n"
    header += "|---|---|---|---|---|\n"

    grouped = defaultdict(list)
    for item in summary:
        grouped[item['category']].append(item)

    misc_bucket = []
    filtered = {}
    for category, items in grouped.items():
        if len(items) < min_group_size:
            misc_bucket.extend(items)
        else:
            filtered[category] = items
    if misc_bucket:
        filtered['MISC'] = filtered.get('MISC', []) + misc_bucket

    sections = []
    for category in sorted(filtered.keys()):
        rows = []
        for item in sorted(filtered[category], key=lambda x: x['name']):
            desc = item['description']
            val = item['value'] or '—'
            modules = item['modules'] or '—'
            rows.append(
                f"| `{item['name']}` | {desc.replace('|', '\\|')} | {val.replace('|', '\\|')} | {modules} | {item['definition']} |"
            )
        section_md = header + "\n".join(rows)
        sections.append(f"\n\n### {category}\n\n" + section_md)

    md = "\n".join(sections)
    md_path = ROOT / 'scratch' / 'MICROPY_macros.md'
    md_path.write_text(md)
    return md_path

summary_ai = build_summary_with_ai()
md_path = render_markdown_with_ai(summary_ai)
md_path


