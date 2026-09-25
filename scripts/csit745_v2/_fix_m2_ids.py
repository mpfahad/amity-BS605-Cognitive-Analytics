"""Normalize M2 concept ids from m2-2.x.x to 2.x.x; keep question ids m2-...-qN."""
from pathlib import Path

p = Path(__file__).with_name("write_m2_pack.py")
s = p.read_text(encoding="utf-8")
out = []
i = 0
while i < len(s):
    if s.startswith('"m2-2.', i):
        end = s.find('"', i + 1)
        token = s[i + 1 : end]
        if "-q" in token:
            out.append(s[i : end + 1])
        else:
            out.append('"' + token[3:] + '"')
        i = end + 1
        continue
    out.append(s[i])
    i += 1
text = "".join(out)
p.write_text(text, encoding="utf-8")
print("normalized", text.count('"2.1.1"'), "refs to 2.1.1")
print("q id kept", "m2-2.1.1-q1" in text)
