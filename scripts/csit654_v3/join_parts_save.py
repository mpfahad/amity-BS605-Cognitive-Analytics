"""Concatenate dump parts written as _partN.txt into a batch JSON and save."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from save_batch import save_batch

base = Path(sys.argv[1])  # e.g. subjects/.../amigo/_m2
parts = sorted(base.parent.glob(base.name + "_part*.txt"))
text = "".join(p.read_text(encoding="utf-8") for p in parts)
out = Path(str(base) + ".json")
out.write_text(text, encoding="utf-8")
data = json.loads(text)
save_batch(data, sys.argv[2] if len(sys.argv) > 2 else "topic")
print("saved", out, "quizzes", len(data))
