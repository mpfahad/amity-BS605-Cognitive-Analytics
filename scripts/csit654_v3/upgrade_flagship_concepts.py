"""Stamp diagram + stronger worked examples onto flagship concepts."""
from __future__ import annotations

import json
from pathlib import Path

PATH = Path(__file__).resolve().parents[2] / "subjects" / "csit654" / "v3" / "data" / "concepts.json"

DIAGRAMS = {
    "1.1.1": {
        "title": "Attack classification",
        "rows": [
            ["Sender", "→ message →", "Receiver"],
            ["", "↓", ""],
            ["Passive: listen / traffic analysis", "or", "Active: modify / replay / DoS"],
        ],
    },
    "1.1.2": {
        "title": "Services → mechanisms",
        "rows": [
            ["SECURITY REQUIREMENT", "", ""],
            ["Confidentiality", "Integrity", "Authentication"],
            ["↓", "↓", "↓"],
            ["Encryption", "MAC / Hash", "Credentials / Signatures"],
        ],
    },
    "1.1.7": {
        "title": "Steganography vs cryptography",
        "rows": [
            ["Cryptography", "hides meaning", "ciphertext visible"],
            ["Steganography", "hides existence", "cover media looks ordinary"],
        ],
    },
    "2.1.3": {
        "title": "Feistel round (schematic)",
        "rows": [
            ["Lᵢ", "Rᵢ"],
            ["", "↓ F(Rᵢ, Kᵢ)"],
            ["Lᵢ₊₁ = Rᵢ", "Rᵢ₊₁ = Lᵢ ⊕ F(Rᵢ, Kᵢ)"],
            ["Decrypt: same structure, reverse round keys", ""],
        ],
    },
    "2.2.1": {
        "title": "Public-key idea",
        "rows": [
            ["Public key", "→ encrypt / verify →", "Anyone"],
            ["Private key", "→ decrypt / sign →", "Owner only"],
        ],
    },
    "3.1.1": {
        "title": "Hash vs MAC",
        "rows": [
            ["Hash", "no key", "integrity only (detect change)"],
            ["MAC", "shared secret", "integrity + authenticity"],
        ],
    },
    "4.1.1": {
        "title": "Kerberos ticket flow",
        "rows": [
            ["Client", "→ AS →", "TGT"],
            ["Client", "→ TGS →", "Service ticket"],
            ["Client", "→ Server →", "Access"],
        ],
    },
    "5.1.1": {
        "title": "Malware family sketch",
        "rows": [
            ["Virus", "needs host file", "user action to spread"],
            ["Worm", "self-replicates", "network / service exploit"],
            ["Trojan", "disguised useful", "payload after install"],
        ],
    },
}

EXAMPLES = {
    "1.1.1": (
        "**Scenario:** An adversary records only the lengths and times of encrypted VPN sessions "
        "between two offices and never changes a packet. That is **traffic analysis** — still passive. "
        "If they later replay a captured login token, the attack becomes **active**."
    ),
    "1.1.2": (
        "**Scenario:** Fahad sends payroll data to a company server.\n"
        "- Nobody else should read it → **confidentiality** (mechanism: encryption).\n"
        "- Server must detect modification → **integrity** (mechanism: MAC / hash with protection).\n"
        "- Server must verify who sent it → **authentication** (credentials or signatures).\n"
        "Exam habit: name the *service* first, then a plausible *mechanism*."
    ),
    "2.1.3": (
        "**Worked sketch:** One Feistel round swaps halves after mixing: "
        "Lᵢ₊₁ = Rᵢ and Rᵢ₊₁ = Lᵢ ⊕ F(Rᵢ, Kᵢ). "
        "Decryption uses the same round function with keys in reverse order — that is why Feistel "
        "is popular in classical DES-style designs."
    ),
    "4.1.1": (
        "**Ticket walk-through:** Client authenticates to the AS and receives a TGT. "
        "With the TGT, the client asks the TGS for a service ticket. "
        "The service ticket is then presented to the application server — the server never sees the password."
    ),
}


def main() -> None:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    concepts = data["concepts"]
    n_d = n_e = 0
    for cid, diagram in DIAGRAMS.items():
        if cid not in concepts:
            continue
        concepts[cid]["diagram"] = diagram
        n_d += 1
    for cid, example in EXAMPLES.items():
        if cid in concepts and concepts[cid].get("learn"):
            concepts[cid]["learn"]["example"] = example
            n_e += 1
    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"diagrams={n_d} examples={n_e}")


if __name__ == "__main__":
    main()
