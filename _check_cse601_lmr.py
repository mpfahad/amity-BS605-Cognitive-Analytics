# -*- coding: utf-8 -*-
import json
import re
from pathlib import Path

maps = json.loads(Path("subjects/cse601/_module_maps.json").read_text(encoding="utf-8"))
deep = json.loads(Path("subjects/cse601/_deep_notes.json").read_text(encoding="utf-8"))

print("=== MAP nodes with lmr=true ===")
for m in maps["modules"]:
    print(f"Module {m['id']} weight={m.get('weight')}")
    for lv in m["levels"]:
        for n in lv["nodes"]:
            if n.get("lmr"):
                tid = str(n.get("topicId") or n["id"])
                d = deep.get(tid, {})
                print(f"  MAP  {tid:8} {n['title'][:42]:42} deep.lmr={d.get('lmr')}")

map_lmr = set()
for m in maps["modules"]:
    for lv in m["levels"]:
        for n in lv["nodes"]:
            if n.get("lmr"):
                map_lmr.add(str(n.get("topicId") or n["id"]))

deep_lmr = {
    k
    for k, v in deep.items()
    if isinstance(v, dict) and v.get("lmr") and re.match(r"^\d", k)
}
print("deep only", sorted(deep_lmr - map_lmr))
print("map only", sorted(map_lmr - deep_lmr))
print("both", sorted(map_lmr & deep_lmr))

# Also check HTML embedded MAPS nodes.lmr vs levels
html = Path("subjects/cse601/module-map.html").read_text(encoding="utf-8")
# crude: find lmr true counts in levels portion
import re as _re
true_count = len(_re.findall(r'"lmr": true', html))
false_count = len(_re.findall(r'"lmr": false', html))
print(f"HTML lmr true={true_count} false={false_count}")
