"""Normalize M4/M5 concept ids to syllabus form (4.x.y / 5.x.y).

Keeps question ids prefixed (m4-...-qN, m5-...-a/b/c).
Also fixes C()/Q() helpers and tree node ids to match M2/M3 style.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fix_m4(text: str) -> str:
    # Helpers: concept id = section; question id keeps m4- prefix
    text = text.replace('cid = f"m4-{section}"', "cid = section")
    text = text.replace('"conceptId": f"m4-{section}"', '"conceptId": section')
    text = text.replace('status="draft"', 'status="approved"')

    def repl(m: re.Match) -> str:
        token = m.group(1)
        # question ids: m4-4.x.y-qN
        if re.search(r"-q\d+$", token):
            return f'"{token}"'
        # strip m4- from concept / tree / related refs
        if token.startswith("m4-"):
            return f'"{token[3:]}"'
        return f'"{token}"'

    text = re.sub(r'"((?:m4-)?4\.\d+(?:\.\d+)*)"', repl, text)
    # also catch related list items already rewritten? handled above
    return text


def fix_m5(text: str) -> str:
    def repl(m: re.Match) -> str:
        token = m.group(1)
        # question ids: m5-5.x.y-a / -b / -c / -qN
        if re.search(r"-(?:q\d+|[abc])$", token):
            return f'"{token}"'
        if token.startswith("m5-"):
            return f'"{token[3:]}"'
        return f'"{token}"'

    text = re.sub(r'"((?:m5-)?5\.\d+(?:\.\d+)*)"', repl, text)
    # Q(qid, concept_id) second args that are still m5-... without suffix
    text = re.sub(
        r'(Q\("[^"]+",\s*)"m5-(5\.\d+(?:\.\d+)*)"',
        r'\1"\2"',
        text,
    )
    return text


def main() -> None:
    m4 = HERE / "write_m4_pack.py"
    m5 = HERE / "write_m5_pack.py"
    t4 = fix_m4(m4.read_text(encoding="utf-8"))
    t5 = fix_m5(m5.read_text(encoding="utf-8"))
    m4.write_text(t4, encoding="utf-8")
    m5.write_text(t5, encoding="utf-8")
    print("m4 concept key 4.1.1:", '"4.1.1"' in t4 and '"m4-4.1.1"' not in t4.replace("m4-4.1.1-q", ""))
    print("m4 q id kept:", "m4-4.1.1-q1" in t4)
    print("m4 status approved:", 'status="approved"' in t4)
    print("m5 concept key 5.1.1:", '"5.1.1"' in t5)
    print("m5 leftover m5-5.1.1 concept (no suffix):", bool(re.search(r'"m5-5\.\d+\.\d+"', t5)))
    print("m5 q id kept:", "m5-5.1.1-a" in t5)


if __name__ == "__main__":
    main()
