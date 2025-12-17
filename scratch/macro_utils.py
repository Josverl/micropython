
def module_hint(relpath: str) -> str:
    parts = relpath.split('/')
    if not parts:
        return ''
    if parts[0] == 'ports' and len(parts) > 1:
        return f"ports/{parts[1]}"
    return parts[0]


def macro_category(name: str) -> str:
    # Extract token after MICROPY_
    rest = name.removeprefix('MICROPY_')
    token = rest.split('_', 1)[0]
    return token or 'MISC'


def choose_best_description(defs_for_name):
    # defs_for_name: list of dicts with keys description, comment, value, file, line
    # Prefer non-empty description, else longest comment, else longest value, else first
    descr_candidates = [d for d in defs_for_name if d.get('description')]
    if descr_candidates:
        descr_candidates.sort(key=lambda d: len(d['description']), reverse=True)
        return descr_candidates[0]['description'], f"{descr_candidates[0]['file']}:{descr_candidates[0]['line']}"
    comment_candidates = [d for d in defs_for_name if d.get('comment')]
    if comment_candidates:
        comment_candidates.sort(key=lambda d: len(d['comment']), reverse=True)
        return comment_candidates[0]['comment'], f"{comment_candidates[0]['file']}:{comment_candidates[0]['line']}"
    value_candidates = [d for d in defs_for_name if d.get('value')]
    if value_candidates:
        value_candidates.sort(key=lambda d: len(d['value']), reverse=True)
        return value_candidates[0]['value'], f"{value_candidates[0]['file']}:{value_candidates[0]['line']}"
    first = defs_for_name[0]
    return '', f"{first['file']}:{first['line']}"