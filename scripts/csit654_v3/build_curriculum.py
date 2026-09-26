"""Build curriculum.json from _module_maps.json for CSIT654 v3 LMS."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / "subjects" / "csit654" / "_module_maps.json"
OUT = ROOT / "subjects" / "csit654" / "v3" / "data" / "curriculum.json"

MODULE_META = {
    1: {
        "title": "Introduction to Network Security",
        "short": "Network Security Foundations",
        "blurb": "Threats, attacks, services, classical encryption, and hardware security.",
        "color": "m1",
    },
    2: {
        "title": "Secret & Public Key Cryptography",
        "short": "Cryptography",
        "blurb": "Block ciphers, Feistel, DES, AES, number theory, and RSA.",
        "color": "m2",
    },
    3: {
        "title": "Authentication Standards & Key Management",
        "short": "Authentication & Integrity",
        "blurb": "MAC, hashing, SHA, message digests, and digital signatures.",
        "color": "m3",
    },
    4: {
        "title": "Web Security",
        "short": "Web & Communication Security",
        "blurb": "Kerberos, ACL, PGP, S/MIME, IPsec, SSL/TLS, SET.",
        "color": "m4",
    },
    5: {
        "title": "System Security & Forensics",
        "short": "System Security & Forensics",
        "blurb": "IDS, malware, firewalls, VPN, blockchain, cyber forensics.",
        "color": "m5",
    },
}


def clean_title(t: str) -> str:
    t = (t or "").strip()
    # Fix truncated titles from map scrape
    fixes = {
        "Modern Block Ciphers: Block Ciphers Princi": "Modern Block Ciphers: Principles",
        "Shannon’s Theory of Confusion and Diffusio": "Shannon’s Theory of Confusion and Diffusion",
        "Fiestal Structure": "Feistel Structure",
        "Introduction of Message Authentication Cod": "Introduction of Message Authentication Codes",
        "Electronic Mail Security: Pretty Good Priv": "Electronic Mail Security: Pretty Good Privacy (PGP)",
        "Recent Network Attacks and Security Measur": "Recent Network Attacks and Security Measures",
    }
    return fixes.get(t, t)


def main() -> None:
    maps = json.loads(MAPS.read_text(encoding="utf-8"))
    modules = []
    for m in maps["modules"]:
        mid = int(m["id"])
        meta = MODULE_META[mid]
        topics = []
        for level in m.get("levels") or []:
            for node in level.get("nodes") or []:
                topics.append(
                    {
                        "id": node["id"],
                        "title": clean_title(node.get("title") or node["id"]),
                        "group": node.get("sub") or "",
                        "lmr": bool(node.get("lmr")),
                    }
                )
        modules.append(
            {
                "id": mid,
                "title": meta["title"],
                "short": meta["short"],
                "blurb": meta["blurb"],
                "color": meta["color"],
                "topicCount": len(topics),
                "topics": topics,
            }
        )
    payload = {
        "subject": "csit654",
        "code": "CSIT654",
        "title": "Network Security & Cryptography",
        "progressKey": "csit654_v3",
        "modules": modules,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} modules={len(modules)} topics={sum(len(m['topics']) for m in modules)}")


if __name__ == "__main__":
    main()
