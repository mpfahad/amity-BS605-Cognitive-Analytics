import json
from pathlib import Path

ROOT = Path("subjects/csit654/v3/source/amigo")


def save_batch(results, kind="topic"):
    outdir = ROOT / kind
    outdir.mkdir(parents=True, exist_ok=True)
    for item in results:
        cmid = str(item["cmid"])
        path = outdir / f"{cmid}.json"
        payload = {
            "cmid": cmid,
            "status": item.get("status"),
            "from": item.get("from"),
            "url": item.get("url"),
            "note": item.get("note"),
            "questions": item.get("questions") or [],
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(cmid, payload["status"], len(payload["questions"]))


if __name__ == "__main__":
    import sys

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    save_batch(data, sys.argv[2] if len(sys.argv) > 2 else "topic")
