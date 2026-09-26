# -*- coding: utf-8 -*-
"""Write original Learn/Revise lessons for CSIT654 v3 Modules 1–2."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "subjects" / "csit654" / "v3" / "data" / "concepts_m1m2.json"

CONCEPTS: dict = {}


def add(c: dict) -> None:
    CONCEPTS[c["id"]] = c


# ---------------------------------------------------------------------------
# Module 1
# ---------------------------------------------------------------------------

add(
    {
        "id": "1.1.1",
        "title": "Introduction to Security Attacks",
        "module": 1,
        "group": "Network security",
        "lmr": True,
        "tags": ["passive", "active", "CIA", "traffic-analysis", "DoS"],
        "learn": {
            "concept": (
                "A security attack is any action that threatens confidentiality, integrity, or availability of "
                "information or systems. Textbooks split attacks into passive (observe without changing "
                "resources) and active (alter data, processes, or availability). Exam stems usually ask you "
                "to classify the behaviour first, then map it to CIA."
            ),
            "howItWorks": (
                "Passive attacks\n"
                "- Goal: learn what is being sent or who talks to whom.\n"
                "- Release of message contents: read email, files, calls.\n"
                "- Traffic analysis: even with encryption, timing, length, and endpoints leak patterns.\n"
                "- Hard to detect (nothing is changed); prevention (encryption, traffic padding) matters more.\n\n"
                "Active attacks\n"
                "- Masquerade: pretend to be another entity.\n"
                "- Replay: capture then resend to produce an unauthorised effect.\n"
                "- Modification: change, delay, or reorder messages.\n"
                "- Denial of service: block or overload a service.\n\n"
                "CIA asset view\n"
                "- Interception → confidentiality.\n"
                "- Modification / fabrication → integrity.\n"
                "- Interruption → availability."
            ),
            "example": (
                "Scenario: an adversary records only the lengths and times of encrypted VPN sessions between "
                "two offices and never changes a packet. That is traffic analysis — still passive. If they later "
                "replay a captured login token, the attack becomes active."
            ),
            "compare": [
                {
                    "title": "Passive",
                    "bullets": [
                        "Observes or analyses traffic",
                        "Does not alter system resources",
                        "Hard to detect; focus on prevention",
                        "Examples: eavesdropping, traffic analysis",
                    ],
                },
                {
                    "title": "Active",
                    "bullets": [
                        "Modifies, fabricates, replays, or interrupts",
                        "Changes behaviour or availability",
                        "Detection and recovery matter",
                        "Examples: masquerade, message edit, DoS",
                    ],
                },
            ],
            "remember": [
                "“Only listening / sniffing” → passive; “altering packets” → active.",
                "Traffic analysis is passive even when no plaintext is recovered.",
                "DoS / crash service → interruption (availability), not interception.",
                "Fabrication inserts a fake object; modification changes an existing one.",
                "Masquerade and replay are active authenticity/integrity threats.",
            ],
        },
        "revise": {
            "bullets": [
                "Passive = observe; active = alter or disrupt.",
                "Interception→C, modification/fabrication→I, interruption→A.",
                "Traffic analysis stays passive.",
                "Masquerade, replay, modification, DoS are the classic active set.",
                "Prevention for passive; detection + recovery for active.",
            ],
            "flash": [
                {"q": "Passive vs active in one line?", "a": "Passive learns without changing resources; active changes data, process, or availability."},
                {"q": "Is traffic analysis passive or active?", "a": "Passive — patterns are observed; resources are not altered."},
                {"q": "Interruption attacks which CIA goal?", "a": "Availability (asset destroyed, blocked, or overloaded)."},
                {"q": "Replay of a captured auth message?", "a": "Active attack (unauthorised effect from re-sending)."},
            ],
        },
        "related": ["1.1.2", "1.1.6"],
    }
)

add(
    {
        "id": "1.1.2",
        "title": "Services and Mechanism",
        "module": 1,
        "group": "Network security",
        "lmr": True,
        "tags": ["service", "mechanism", "confidentiality", "authentication", "non-repudiation"],
        "learn": {
            "concept": (
                "A security service is the protection goal you want (confidentiality, integrity, authentication, "
                "non-repudiation, access control, availability). A security mechanism is the concrete process "
                "or device that detects, prevents, or recovers from attacks. Exam questions almost always test "
                "this what-versus-how split."
            ),
            "howItWorks": (
                "Core message/entity services\n"
                "- Confidentiality: only intended parties can read the content (typically via encipherment).\n"
                "- Integrity: data arrives unaltered; often supported by checksums/MACs.\n"
                "- Authentication: prove the claimed sender or user identity.\n"
                "- Non-repudiation: a party cannot later deny a prior action; usually needs signatures/TTP.\n"
                "- Entity authentication: verify the user before granting service access.\n\n"
                "Example mechanisms from the SLM\n"
                "- Encipherment, access control, notarization, data integrity checks,\n"
                "  authentication exchange, digital signatures.\n\n"
                "Mapping rule\n"
                "- One mechanism can support several services (encryption aids secrecy and can feed integrity).\n"
                "- One service may need several mechanisms (non-repudiation needs more than a plain MAC)."
            ),
            "example": (
                "Stem: “Which security service ensures the receiver knows the real sender?” Answer: "
                "authentication (service). AES or a password challenge would be mechanisms that help implement it."
            ),
            "compare": [
                {
                    "title": "Security service",
                    "bullets": [
                        "Abstract goal / “what we want”",
                        "Names: confidentiality, integrity, authentication, non-repudiation…",
                        "Exam cue: not an algorithm name",
                    ],
                },
                {
                    "title": "Security mechanism",
                    "bullets": [
                        "Concrete technique / “how”",
                        "Examples: cipher, MAC, signature, firewall, PIN",
                        "Exam cue: tool or process, not CIA label alone",
                    ],
                },
            ],
            "remember": [
                "Service = goal; mechanism = technique.",
                "Stem asks for a service → confidentiality/authentication/… not “AES”.",
                "Stem asks for a mechanism → cipher, hash, signature, firewall, etc.",
                "Authentication ≠ authorisation (identity proof vs permission).",
                "Non-repudiation usually needs signatures or a trusted third party — not only a MAC.",
            ],
        },
        "revise": {
            "bullets": [
                "Services name protection goals; mechanisms implement them.",
                "Confidentiality ↔ encipherment is the classic pairing.",
                "Integrity often uses appended check values; authentication proves origin.",
                "Non-repudiation is stronger than “I have the message”.",
                "One-to-many mapping both ways between services and mechanisms.",
            ],
            "flash": [
                {"q": "Service vs mechanism?", "a": "Service = security goal; mechanism = process/device that achieves it."},
                {"q": "Name four message-oriented services.", "a": "Confidentiality, integrity, authentication, non-repudiation."},
                {"q": "Is encryption a service or a mechanism?", "a": "Mechanism (encipherment) that mainly supports confidentiality."},
                {"q": "Why is a MAC alone weak for non-repudiation?", "a": "Both parties share the key; either could have made the tag."},
            ],
        },
        "related": ["1.1.1", "1.1.3"],
    }
)

add(
    {
        "id": "1.1.3",
        "title": "Classical Encryption Techniques",
        "module": 1,
        "group": "Network security",
        "lmr": True,
        "tags": ["plaintext", "ciphertext", "key", "symmetric", "Kerckhoffs"],
        "learn": {
            "concept": (
                "Classical encryption covers pre-computer and early electromechanical schemes built mainly from "
                "substitution and transposition under a shared secret key. Know the five ingredients of a "
                "symmetric model: plaintext, encryption algorithm, secret key, ciphertext, decryption algorithm. "
                "Modern practice assumes Kerckhoffs: algorithm public, key secret."
            ),
            "howItWorks": (
                "Symmetric model\n"
                "- Y = E(K, X); X = D(K, Y).\n"
                "- Same key must reach sender and receiver securely and stay secret.\n"
                "- Adversary is assumed to know E and D and to observe Y.\n\n"
                "Two classical families\n"
                "- Substitution: replace symbols (Caesar, Playfair, Vigenère).\n"
                "- Transposition: reorder positions (rail fence, columnar).\n"
                "- Product ciphers stack stages (later rotor machines / modern rounds).\n\n"
                "Security requirements (from the SLM)\n"
                "- Strong algorithm: ciphertext alone (or with known plaintext) should not yield key/plaintext.\n"
                "- Secure key distribution and storage — key compromise opens all traffic under that key.\n"
                "- Brute force: try keys until plaintext looks meaningful (~half the key space on average)."
            ),
            "example": (
                "Exam habit: first name plaintext/ciphertext/key, then say whether the stem describes "
                "replacement (substitution) or reordering (transposition). Do not shrink “classical” to only Caesar."
            ),
            "compare": [
                {
                    "title": "Substitution",
                    "bullets": [
                        "Changes symbol identity",
                        "Letter frequencies often preserved (monoalphabetic)",
                        "Cue: “replace letters”",
                    ],
                },
                {
                    "title": "Transposition",
                    "bullets": [
                        "Changes only order",
                        "Same letters/frequencies remain",
                        "Cue: “rearrange letters”",
                    ],
                },
            ],
            "remember": [
                "Classical crypto ≈ substitution + transposition under a shared key.",
                "Cryptography designs schemes; cryptanalysis breaks or stress-tests them.",
                "Kerckhoffs: assume the adversary knows the algorithm.",
                "Secure use needs a strong algorithm and a protected secret key.",
                "Caesar is one substitution instance — not the whole topic.",
            ],
        },
        "revise": {
            "bullets": [
                "Five ingredients: plaintext, algorithm, key, ciphertext, decryption.",
                "Y=E(K,X), X=D(K,Y) under a shared K.",
                "Substitution vs transposition is the first branching question.",
                "Kerckhoffs: algorithm public, key secret.",
                "Brute force needs a way to recognise valid plaintext.",
            ],
            "flash": [
                {"q": "Plaintext vs ciphertext?", "a": "Original message vs encoded/encrypted form."},
                {"q": "What must be secret in a modern cipher?", "a": "The key (algorithm is assumed public)."},
                {"q": "Stem “rearrange letters”?", "a": "Transposition cipher."},
                {"q": "Cryptography vs cryptanalysis?", "a": "Design of ciphers vs attacking/analysing them."},
            ],
        },
        "related": ["1.1.4", "1.1.5", "1.1.6"],
    }
)

add(
    {
        "id": "1.1.4",
        "title": "Substitution Ciphers",
        "module": 1,
        "group": "Network security",
        "lmr": False,
        "tags": ["Caesar", "Playfair", "Vigenère", "monoalphabetic", "polyalphabetic"],
        "learn": {
            "concept": (
                "A substitution cipher replaces plaintext units with ciphertext units by a mapping. "
                "Monoalphabetic schemes use one fixed alphabet for the whole message; polyalphabetic "
                "schemes change alphabets with position (Vigenère). Classic syllabus set: Caesar, Playfair, "
                "polyalphabetic/Vigenère, and the one-time pad idea."
            ),
            "howItWorks": (
                "Caesar / shift\n"
                "- C = (p + k) mod 26; P = (C − k) mod 26; nontrivial k ∈ 1..25.\n"
                "- Tiny key space → trivial brute force; frequencies unchanged.\n\n"
                "Playfair\n"
                "- Digraph cipher on a 5×5 keyword square (I/J shared).\n"
                "- Rules: same row → right neighbour; same column → below; else rectangle corners.\n"
                "- Stronger than simple letter substitution (676 digraphs vs 26 letters).\n\n"
                "Polyalphabetic / Vigenère\n"
                "- Repeating keyword selects which Caesar shift applies at each position.\n"
                "- Flattens single-letter frequencies; still breakable (Kasiski / Friedman).\n\n"
                "One-time pad\n"
                "- Random keystream as long as the message, used once, XOR (or mod-26).\n"
                "- Information-theoretically strong if key is truly random and never reused; impractical at scale."
            ),
            "example": (
                "Caesar with k=3: “pay more money” → “SDB PRUH PRQHB”. For Vigenère, align a repeating "
                "keyword under the plaintext and look up each (key letter, plaintext letter) pair."
            ),
            "compare": [
                {
                    "title": "Monoalphabetic",
                    "bullets": [
                        "One mapping for the whole message",
                        "Preserves letter frequencies",
                        "Easy frequency analysis",
                        "Example: Caesar, simple alphabet cipher",
                    ],
                },
                {
                    "title": "Polyalphabetic",
                    "bullets": [
                        "Mapping varies with position/key",
                        "Hides single-letter frequencies somewhat",
                        "Still not “unbreakable” in practice",
                        "Example: Vigenère",
                    ],
                },
            ],
            "remember": [
                "Stem “shift by 3 / ROT” → Caesar.",
                "Stem “one mapping for all letters” → monoalphabetic.",
                "Playfair works on pairs (digraphs), not single letters.",
                "Polyalphabetic ≠ unbreakable — Kasiski still applies.",
                "OTP security collapses if the keystream is reused.",
            ],
        },
        "revise": {
            "bullets": [
                "Substitution replaces symbols by a keyed mapping.",
                "Caesar: C=(p+k) mod 26; only 25 nontrivial keys.",
                "Playfair: 5×5 digraph cipher; stronger frequency profile.",
                "Vigenère: repeating keyword of Caesar shifts.",
                "OTP: perfect if key is random, secret, and one-time.",
            ],
            "flash": [
                {"q": "General Caesar formula?", "a": "C=(p+k) mod 26; decrypt with (C−k) mod 26."},
                {"q": "Why is monoalphabetic weak?", "a": "Ciphertext keeps plaintext letter-frequency patterns."},
                {"q": "Playfair unit of encryption?", "a": "Letter pairs (digraphs) on a 5×5 square."},
                {"q": "OTP reuse danger?", "a": "XOR of two ciphertexts cancels the keystream and leaks plaintext relation."},
            ],
        },
        "related": ["1.1.3", "1.1.5", "1.1.6"],
    }
)

add(
    {
        "id": "1.1.5",
        "title": "Transposition Ciphers",
        "module": 1,
        "group": "Network security",
        "lmr": False,
        "tags": ["rail-fence", "columnar", "permutation", "product-cipher"],
        "learn": {
            "concept": (
                "A transposition cipher permutes positions of plaintext symbols; the symbols themselves stay "
                "the same. Letter frequencies are unchanged, so pure transposition is easy to spot, but "
                "multiple stages (product transposition) make reconstruction harder."
            ),
            "howItWorks": (
                "Rail fence\n"
                "- Write plaintext in a zigzag across a fixed number of rails; read off by rows.\n"
                "- Key is often the rail count.\n\n"
                "Columnar transposition\n"
                "- Write plaintext into a rectangle by rows.\n"
                "- Read columns in an order given by a keyword (alphabetical order of letters).\n"
                "- Keyword orders columns — it is not a substitution alphabet.\n\n"
                "Cryptanalysis cues\n"
                "- Same bag of letters as plaintext → think transposition.\n"
                "- Anagramming / multiple anagramming on short texts.\n"
                "- Combined with substitution → classical product cipher."
            ),
            "example": (
                "Rail fence style: plaintext “meet at the school house” written on diagonals and read by rows "
                "yields a scrambled string with the same letters. Columnar: keyword “ZEBRAS” sorts columns "
                "into a read order."
            ),
            "compare": [
                {
                    "title": "Substitution",
                    "bullets": [
                        "Changes which symbol appears",
                        "Frequencies of letters change labels",
                        "Cue: replace / map letters",
                    ],
                },
                {
                    "title": "Transposition",
                    "bullets": [
                        "Only reorders symbols",
                        "Letter frequencies unchanged",
                        "Cue: same letters, different order",
                    ],
                },
            ],
            "remember": [
                "Stem “same letters, different order” → transposition.",
                "Keyword in columnar cipher orders columns — not a letter substitution.",
                "Rail fence key ≈ number of rails.",
                "Pure transposition keeps frequencies; digraph/position stats change.",
                "Multiple transposition stages strengthen classical schemes.",
            ],
        },
        "revise": {
            "bullets": [
                "Transposition = permute positions only.",
                "Rail fence: zigzag write, row read.",
                "Columnar: row write, key-ordered column read.",
                "Frequencies of letters survive; order does not.",
                "Product ciphers mix substitution + transposition.",
            ],
            "flash": [
                {"q": "What stays the same in pure transposition?", "a": "The multiset of letters (frequencies)."},
                {"q": "Rail fence key?", "a": "Usually the number of rails (zigzag depth)."},
                {"q": "Columnar keyword role?", "a": "Defines the order in which columns are read."},
                {"q": "Why is single-stage transposition weak?", "a": "Anagramming recovers likely plaintext order."},
            ],
        },
        "related": ["1.1.3", "1.1.4", "1.1.8"],
    }
)

add(
    {
        "id": "1.1.6",
        "title": "Cryptanalysis",
        "module": 1,
        "group": "Network security",
        "lmr": False,
        "tags": ["ciphertext-only", "known-plaintext", "chosen-plaintext", "brute-force", "side-channel"],
        "learn": {
            "concept": (
                "Cryptanalysis recovers plaintext and/or key by exploiting weaknesses in ciphers or their "
                "implementation. Always state the attack model: what the adversary can observe or choose. "
                "Cryptography and cryptanalysis together form cryptology — designers use attack results to "
                "harden algorithms."
            ),
            "howItWorks": (
                "Attack models (increasing power)\n"
                "- Ciphertext-only: only Y known.\n"
                "- Known-plaintext: some (X, Y) pairs known.\n"
                "- Chosen-plaintext: attacker can encrypt chosen X.\n"
                "- Chosen-ciphertext: attacker can decrypt chosen Y.\n\n"
                "Methods you should name\n"
                "- Brute force / exhaustive key search (needs plaintext recognition).\n"
                "- Frequency analysis (monoalphabetic); Kasiski (Vigenère).\n"
                "- Differential / integral ideas on block ciphers (chosen-plaintext flavour).\n"
                "- Side-channel: timing, power, EM from the real device — not pure maths of the cipher.\n"
                "- Dictionary, MITM on key exchange, social engineering for keys.\n\n"
                "Design loop\n"
                "- A “break” may fully recover keys or only reduce effective security below the claimed key length."
            ),
            "example": (
                "If the stem says the analyst has matching plaintext–ciphertext pairs and wants the key, "
                "classify known-plaintext — not ciphertext-only. If they can feed chosen messages into an "
                "encryption oracle, it is chosen-plaintext."
            ),
            "compare": [
                {
                    "title": "Ciphertext-only",
                    "bullets": [
                        "Only encrypted messages available",
                        "Weakest model for the attacker",
                        "Classical frequency attacks live here",
                    ],
                },
                {
                    "title": "Known / chosen plaintext",
                    "bullets": [
                        "Pairs or encryption oracle available",
                        "Much stronger attacker",
                        "Modern ciphers must resist these too",
                    ],
                },
            ],
            "remember": [
                "Stem lists known pairs → known-plaintext, not ciphertext-only.",
                "Cryptanalysis ≠ only brute force.",
                "Exhaustive search cost scales with key-space size.",
                "Side-channel leaks from hardware behaviour, not from the equation alone.",
                "Security claims must name the assumed attack model.",
            ],
        },
        "revise": {
            "bullets": [
                "Cryptanalysis = break or weaken ciphers without the intended key.",
                "Models: ciphertext-only < known < chosen.",
                "Brute force needs recognisable plaintext.",
                "Classical: frequency / Kasiski; modern: differential, linear, side-channel.",
                "Results feed back into stronger designs.",
            ],
            "flash": [
                {"q": "Ciphertext-only attack?", "a": "Adversary has only ciphertext (no plaintext, no key)."},
                {"q": "Chosen-plaintext attack?", "a": "Adversary can encrypt chosen plaintexts and study outputs."},
                {"q": "Side-channel attack source?", "a": "Timing, power, EM, or other physical leakage of the device."},
                {"q": "Average brute-force tries?", "a": "About half the key space before success (on average)."},
            ],
        },
        "related": ["1.1.3", "1.1.4", "2.1.6"],
    }
)

add(
    {
        "id": "1.1.7",
        "title": "Steganography",
        "module": 1,
        "group": "Network security",
        "lmr": False,
        "tags": ["cover", "payload", "LSB", "steganalysis", "hide-presence"],
        "learn": {
            "concept": (
                "Steganography hides the existence of a secret payload inside innocent cover media "
                "(image, audio, video, document). Cryptography hides meaning; steganography hides presence. "
                "They are often combined: encrypt first, then embed."
            ),
            "howItWorks": (
                "Vocabulary\n"
                "- Cover: carrier before embedding.\n"
                "- Stego-object: carrier after embedding.\n"
                "- Payload: the hidden data.\n\n"
                "Common methods (SLM)\n"
                "- LSB / least-significant-bit embedding in images or audio.\n"
                "- Palette-based embedding in image palettes.\n"
                "- Secure cover selection: pick a cover whose blocks already resemble the payload pattern.\n\n"
                "Detection\n"
                "- Steganalysis (StegExpose, hex inspection, statistical tests).\n"
                "- Trade-off: capacity vs undetectability.\n"
                "- Goals differ from watermarking (ownership/integrity marking vs secret messaging)."
            ),
            "example": (
                "Malware authors embed code in celebrity JPEGs or WAV files; the download looks harmless until "
                "a dropper extracts the payload. Exam cue: if the stem stresses “nobody notices a message "
                "exists,” answer steganography — not encryption alone."
            ),
            "compare": [
                {
                    "title": "Cryptography",
                    "bullets": [
                        "Hides meaning of a known message",
                        "Ciphertext is usually obvious as ciphertext",
                        "Security from key / hard problems",
                    ],
                },
                {
                    "title": "Steganography",
                    "bullets": [
                        "Hides that a message exists",
                        "Cover looks ordinary",
                        "Security from undetectability of embedding",
                    ],
                },
            ],
            "remember": [
                "Stem “hide that a message exists” → steganography.",
                "Stem “make message unreadable” → cryptography.",
                "LSB embedding is the classic image technique.",
                "Detecting stego ≠ recovering a cipher’s plaintext.",
                "Capacity vs undetectability is the usual trade-off.",
            ],
        },
        "revise": {
            "bullets": [
                "Stego hides presence inside a cover.",
                "Crypto hides meaning; often used together.",
                "LSB / palette / cover-selection are syllabus methods.",
                "Steganalysis tries to detect embedding.",
                "Watermarking is related but serves a different goal.",
            ],
            "flash": [
                {"q": "Cover vs stego-object?", "a": "Innocent carrier before vs after the payload is embedded."},
                {"q": "LSB steganography?", "a": "Replace least-significant bits of media samples with payload bits."},
                {"q": "Crypto vs stego one-liner?", "a": "Crypto hides meaning; stego hides existence."},
                {"q": "What is steganalysis?", "a": "Detecting (and sometimes extracting) hidden stego payloads."},
            ],
        },
        "related": ["1.1.3", "1.1.8"],
    }
)

add(
    {
        "id": "1.1.8",
        "title": "Stream and Block Ciphers",
        "module": 1,
        "group": "Network security",
        "lmr": False,
        "tags": ["stream", "block", "keystream", "XOR", "padding"],
        "learn": {
            "concept": (
                "Stream ciphers transform plaintext one symbol/bit at a time, typically by XOR with a "
                "keystream. Block ciphers transform fixed-size blocks (e.g. 64 or 128 bits) under one key. "
                "Most modern symmetric encryption is built on block ciphers; modes (Module 2) turn blocks "
                "into message encryption."
            ),
            "howItWorks": (
                "Stream ciphers\n"
                "- Fast, constant space; low error propagation across symbols.\n"
                "- Weak diffusion: each ciphertext symbol mainly depends on one plaintext symbol.\n"
                "- Keystream reuse is catastrophic (two ciphertexts XOR → plaintext relation).\n"
                "- Synchronous: keystream independent of ciphertext; self-synchronising: depends on prior ciphertext.\n\n"
                "Block ciphers\n"
                "- Encrypt n-bit blocks; need padding if length is not a multiple of n.\n"
                "- High diffusion inside the block; harder to insert undetected symbols.\n"
                "- Slower start (need a full block); bit errors can corrupt a whole block or chained blocks.\n\n"
                "SLM framing tip\n"
                "- Simple substitution ≈ stream-like; pure transposition ≈ block-like classical analogy."
            ),
            "example": (
                "OTP is the ideal stream idea with a truly random one-time keystream. AES-128 encrypts "
                "128-bit chunks — that is a block cipher; AES-CTR then builds a stream-like keystream from it."
            ),
            "compare": [
                {
                    "title": "Stream cipher",
                    "bullets": [
                        "Bit/byte at a time + keystream",
                        "Low latency; no block padding",
                        "Weak diffusion; reuse is fatal",
                        "Error often local to a symbol",
                    ],
                },
                {
                    "title": "Block cipher",
                    "bullets": [
                        "Fixed-size blocks under one key",
                        "Strong mixing inside the block",
                        "Needs modes + often padding",
                        "Errors can spoil whole blocks",
                    ],
                },
            ],
            "remember": [
                "Stem “XOR with running keystream” → stream.",
                "Stem “encrypt 64/128-bit chunks” → block.",
                "Never reuse a stream keystream under the same key.",
                "ECB/CBC are modes of block ciphers, not stream ciphers themselves.",
                "Block size choice ≠ key strength; key length drives brute-force cost.",
            ],
        },
        "revise": {
            "bullets": [
                "Stream: sequential; block: fixed chunks.",
                "Stream pros: speed, local errors; cons: diffusion, insertion risk, reuse.",
                "Block pros: diffusion, tamper resistance; cons: latency, padding, block errors.",
                "OTP is perfect stream theory; impractical at scale.",
                "Modern practice: block cipher + mode (often stream-like CTR/GCM).",
            ],
            "flash": [
                {"q": "Stream vs block?", "a": "Stream encrypts symbols continuously; block encrypts fixed-size groups."},
                {"q": "Why is keystream reuse bad?", "a": "C1⊕C2 cancels the keystream and relates the two plaintexts."},
                {"q": "Why padding?", "a": "Message length must become a multiple of the block size."},
                {"q": "DES vs AES block sizes?", "a": "DES 64-bit blocks; AES 128-bit blocks."},
            ],
        },
        "related": ["1.1.3", "2.1.1", "2.1.7"],
    }
)

add(
    {
        "id": "1.1.9",
        "title": "Overview of Hardware Security",
        "module": 1,
        "group": "Network security",
        "lmr": False,
        "tags": ["TPM", "side-channel", "root-of-trust", "secure-boot", "HSM"],
        "learn": {
            "concept": (
                "Hardware security protects systems through physical roots of trust, isolated crypto engines, "
                "and defenses against attacks that target chips and firmware — not only the maths of an "
                "algorithm. Correct software crypto can still leak through timing, power, or EM on real silicon."
            ),
            "howItWorks": (
                "Roots of trust\n"
                "- Immutable ROM / secure boot verifies each later stage upward.\n"
                "- TPM / secure element / HSM: store keys and run crypto off the main CPU.\n\n"
                "Threat themes in the SLM\n"
                "- Hardware Trojans and supply-chain implants.\n"
                "- Side-channels: power, timing, EM (Kocher-style attacks on smart cards, RSA, DSS…).\n"
                "- Formal verification of security protocols’ secrecy/authentication claims.\n\n"
                "Exam framing\n"
                "- Hardware security complements algorithmic strength; it does not replace AES/RSA sizing.\n"
                "- Name one concrete example (TPM, smart card, secure enclave) when asked to “define + example”."
            ),
            "example": (
                "An AES implementation can be mathematically correct yet leak the key via differential power "
                "analysis on a smart card. Mitigations: constant-time code, masking, and keys kept inside a TPM."
            ),
            "compare": None,
            "remember": [
                "Stem “power analysis / timing leak” → side-channel.",
                "Do not assume software AES is automatically safe on embedded devices.",
                "Secure boot chains trust from hardware upward.",
                "TPM/HSM isolate key material from the OS.",
                "Hardware security complements — does not replace — cipher strength.",
            ],
        },
        "revise": {
            "bullets": [
                "Hardware roots of trust anchor secure boot.",
                "TPM/secure element isolate keys and crypto ops.",
                "Side-channels attack physical leakage, not just equations.",
                "Hardware Trojans are supply-chain / implant threats.",
                "Always pair algorithmic crypto with implementation hardening.",
            ],
            "flash": [
                {"q": "What is a hardware root of trust?", "a": "Boot-anchored component that verifies later software stages."},
                {"q": "Side-channel example?", "a": "Recovering a key from power traces or timing of modular exponentiation."},
                {"q": "TPM role?", "a": "Dedicated chip storing keys and performing crypto in isolation."},
                {"q": "Does strong AES math stop side-channels?", "a": "No — implementations can still leak on real hardware."},
            ],
        },
        "related": ["1.1.6", "2.1.5"],
    }
)

# ---------------------------------------------------------------------------
# Module 2 — Secret key
# ---------------------------------------------------------------------------

add(
    {
        "id": "2.1.1",
        "title": "Modern Block Ciphers: Principles",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": True,
        "tags": ["block-cipher", "product-cipher", "rounds", "key-schedule", "avalanche"],
        "learn": {
            "concept": (
                "A modern block cipher is a keyed invertible map on n-bit blocks (typical n = 64 or 128). "
                "Strength comes mainly from key length and round design, not from secrecy of the algorithm. "
                "Because a huge substitution table is impossible, designers build product ciphers from "
                "smaller substitution and permutation layers repeated in rounds."
            ),
            "howItWorks": (
                "Principles\n"
                "- Confusion + diffusion (Shannon) realised via Feistel or SPN structures.\n"
                "- Rounds: repeated keyed mixing; key schedule derives round keys from the master key.\n"
                "- Ideal behaviour: look like a pseudorandom permutation; avalanche (1-bit change flips ~half the bits).\n\n"
                "Design notes from the SLM\n"
                "- Block size does not by itself set strength; key length does for brute force.\n"
                "- Small blocks still enable codebook / birthday issues at large volume.\n"
                "- Modes of operation are separate from the primitive (next topics).\n\n"
                "Named schemes to recognise\n"
                "- DES (64-bit block, short key — legacy), 3DES, AES (Rijndael), IDEA, Twofish, Serpent."
            ),
            "example": (
                "A 64-bit ideal cipher would need a 2^64-entry table — impossible. Instead DES/AES compose "
                "S-boxes and permutations over many rounds. Trap: calling AES a Feistel cipher — AES is SPN; "
                "DES is Feistel."
            ),
            "compare": [
                {
                    "title": "Feistel (e.g. DES)",
                    "bullets": [
                        "Split block L∥R; F on one half",
                        "F need not be invertible",
                        "Encrypt/decrypt share structure (reverse keys)",
                    ],
                },
                {
                    "title": "SPN (e.g. AES)",
                    "bullets": [
                        "Full-block layers each round",
                        "S-box + linear mixing + AddRoundKey",
                        "Encrypt/decrypt use inverse layers",
                    ],
                },
            ],
            "remember": [
                "State block size, key size, rounds, and product-cipher idea.",
                "Avalanche: one-bit change should scramble ciphertext unpredictably.",
                "AES ≠ Feistel; DES = Feistel.",
                "Mode ≠ algorithm (AES-CBC is AES in CBC mode).",
                "Principles come before named algorithms in exam answers.",
            ],
        },
        "revise": {
            "bullets": [
                "Block cipher = keyed permutation on n-bit blocks.",
                "Built as product of substitutions/permutations over rounds.",
                "Key schedule → round keys; avalanche is the quality check.",
                "Feistel vs SPN are the two dominant structures.",
                "Modes turn the primitive into message encryption.",
            ],
            "flash": [
                {"q": "Why product ciphers?", "a": "A full n-bit substitution table is infeasible; compose small layers instead."},
                {"q": "What does the key schedule do?", "a": "Derives per-round subkeys from the master key."},
                {"q": "Avalanche effect?", "a": "Tiny plaintext/key change flips about half the ciphertext bits."},
                {"q": "DES vs AES structure?", "a": "DES is Feistel; AES is an SPN (not Feistel)."},
            ],
        },
        "related": ["1.1.8", "2.1.2", "2.1.3"],
    }
)

add(
    {
        "id": "2.1.2",
        "title": "Shannon’s Theory of Confusion and Diffusion",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": True,
        "tags": ["confusion", "diffusion", "S-box", "avalanche", "Shannon"],
        "learn": {
            "concept": (
                "Claude Shannon required two properties for strong ciphers: confusion (make the ciphertext–key "
                "relation complex) and diffusion (spread plaintext statistical structure across many ciphertext "
                "bits). Either alone is insufficient; modern rounds combine nonlinear S-boxes with linear mixing."
            ),
            "howItWorks": (
                "Confusion\n"
                "- Hide how ciphertext depends on the key.\n"
                "- Primary tool: nonlinear substitution (S-boxes).\n"
                "- Goal: knowing many plaintext–ciphertext pairs still should not reveal the key easily.\n\n"
                "Diffusion\n"
                "- Spread each plaintext (and key) bit’s influence across many output bits.\n"
                "- Primary tool: permutation / MixColumns-style linear mixing.\n"
                "- Strict avalanche: flipping bit i flips bit j with probability ~1/2.\n\n"
                "Concrete links\n"
                "- DES: S-boxes (confusion) + P-permutation (diffusion) inside Feistel rounds.\n"
                "- AES: SubBytes (confusion) + ShiftRows/MixColumns (diffusion).\n"
                "- SLM note: stream ciphers lean on confusion; block ciphers need both."
            ),
            "example": (
                "Stem “hide the key–ciphertext relationship” → confusion. Stem “spread each plaintext bit’s "
                "influence” → diffusion. If asked how AES achieves them, name SubBytes vs MixColumns/ShiftRows."
            ),
            "compare": [
                {
                    "title": "Confusion",
                    "bullets": [
                        "Complex ciphertext ↔ key link",
                        "Nonlinear S-boxes",
                        "Masks key dependence",
                    ],
                },
                {
                    "title": "Diffusion",
                    "bullets": [
                        "Spread plaintext statistics",
                        "Permutation / MixColumns",
                        "Masks plaintext structure; enables avalanche",
                    ],
                },
            ],
            "remember": [
                "Confusion ↔ key complexity; diffusion ↔ spread influence.",
                "Swapping the two definitions is the classic MCQ fail.",
                "S-box without diffusion leaves structure; linear mixing without S-boxes is weak.",
                "Shannon: both properties are required.",
                "Avalanche is the practical test of good diffusion (+ confusion).",
            ],
        },
        "revise": {
            "bullets": [
                "Confusion: obscure key–ciphertext relation (S-boxes).",
                "Diffusion: spread plaintext influence (permutations/mixing).",
                "Both needed; SPNs/Feistel rounds implement them.",
                "DES and AES map layers cleanly onto the two ideas.",
                "Avalanche ≈ flipping one input bit flips ~half the output.",
            ],
            "flash": [
                {"q": "Shannon confusion?", "a": "Make ciphertext–key dependence as complex as possible."},
                {"q": "Shannon diffusion?", "a": "Disperse plaintext redundancy across many ciphertext bits."},
                {"q": "AES confusion layer?", "a": "SubBytes (S-box)."},
                {"q": "AES diffusion layers?", "a": "ShiftRows and MixColumns."},
            ],
        },
        "related": ["2.1.1", "2.1.3", "2.2.1"],
    }
)

add(
    {
        "id": "2.1.3",
        "title": "Feistel Structure",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": True,
        "tags": ["Feistel", "round-function", "DES", "invertibility", "subkeys"],
        "learn": {
            "concept": (
                "The Feistel structure (Horst Feistel / Lucifer lineage) splits a block into halves L∥R and "
                "iterates keyed rounds. It is the backbone of DES and several other ciphers (Blowfish, "
                "CAST-128, KASUMI). Major engineering win: encryption and decryption share the same structure "
                "with round keys reversed."
            ),
            "howItWorks": (
                "Round equations\n"
                "- LE_i = RE_{i−1}\n"
                "- RE_i = LE_{i−1} ⊕ F(RE_{i−1}, K_i)\n"
                "- F is the round function (expansion, S-boxes, permutation in DES); F need not be invertible.\n\n"
                "Why decryption works\n"
                "- XOR undoes the combine step when F’s output is recomputed from the known half and K_i.\n"
                "- Run the same network with subkeys K_n … K_1.\n"
                "- Final L/R swap detail matters for some variants — check the stem.\n\n"
                "Design notes\n"
                "- Number of rounds is a design parameter; weak F is not fixed by “more rounds” alone.\n"
                "- Contrast SPN (AES): whole block mixed each round; inverse layers required."
            ),
            "example": (
                "Exam sketch: draw L0 R0 → rounds → ciphertext halves, write the recurrence, and state "
                "“decrypt = same algorithm, reverse round keys.” That triad scores most Feistel questions."
            ),
            "compare": [
                {
                    "title": "Feistel",
                    "bullets": [
                        "Updates one half per round via F",
                        "F need not be invertible",
                        "Same structure encrypt/decrypt",
                        "Example: DES",
                    ],
                },
                {
                    "title": "SPN (AES)",
                    "bullets": [
                        "Mixes entire block each round",
                        "Layers must be invertible",
                        "Decrypt uses inverse SubBytes/MixColumns…",
                        "Not a Feistel network",
                    ],
                },
            ],
            "remember": [
                "Write LE_i / RE_i and say decryption = reverse keys.",
                "Stem “same algorithm for encrypt/decrypt” → Feistel property.",
                "AES is not Feistel — do not force Feistel equations onto AES.",
                "F needn’t be invertible because XOR undoes the combine.",
                "Correct spelling: Feistel.",
            ],
        },
        "revise": {
            "bullets": [
                "Split block; F(R, K_i) XORed into L; then swap halves.",
                "Decrypt with reversed subkeys on the same network.",
                "F need not be invertible.",
                "DES = 16-round Feistel example.",
                "Feistel ≠ SPN.",
            ],
            "flash": [
                {"q": "Feistel round formulas?", "a": "L_i=R_{i−1}; R_i=L_{i−1}⊕F(R_{i−1},K_i)."},
                {"q": "Why can F be non-invertible?", "a": "Knowing R and K_i recomputes F; XOR recovers the other half."},
                {"q": "Decrypt a Feistel cipher?", "a": "Same structure with round keys in reverse order."},
                {"q": "Is AES Feistel?", "a": "No — AES is an SPN."},
            ],
        },
        "related": ["2.1.1", "2.1.4", "2.2.1"],
    }
)

add(
    {
        "id": "2.1.4",
        "title": "Data Encryption Standard (DES)",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": False,
        "tags": ["DES", "56-bit", "16-rounds", "S-box", "IP"],
        "learn": {
            "concept": (
                "DES is a NIST-standardised 64-bit Feistel block cipher with 16 rounds. The keying material is "
                "64 bits but only 56 bits are effective (8 parity bits). It dominated commercial crypto for "
                "decades and was superseded by AES; Triple DES remained as a transitional option."
            ),
            "howItWorks": (
                "Pipeline\n"
                "- Initial permutation IP → split into LPT/RPT → 16 Feistel rounds → join → final permutation FP (=IP⁻¹).\n"
                "- Decrypt: same algorithm, reverse the 16 subkeys.\n\n"
                "Round f-function\n"
                "- Expand R (32→48), XOR with 48-bit round key, eight 6→4 S-boxes, then P-permutation.\n"
                "- S-boxes supply the main nonlinearity (confusion).\n\n"
                "Key schedule\n"
                "- PC-1, rotations, PC-2 produce sixteen 48-bit subkeys.\n\n"
                "Properties claimed\n"
                "- Avalanche and completeness: each ciphertext bit depends on many plaintext bits.\n"
                "- IP/FP alone add no cryptographic strength — they are fixed permutations."
            ),
            "example": (
                "Fingerprint stem: “56-bit key, 64-bit block, 16 rounds” → DES. Trap: saying the key is "
                "64-bit secure — eight bits are parity only."
            ),
            "compare": None,
            "remember": [
                "DES: 64-bit block, 56-bit effective key, 16 Feistel rounds.",
                "f = E + XOR K_i + S-boxes + P.",
                "Encrypt/decrypt share structure with reversed subkeys.",
                "IP/FP are fixed bookends — not the source of strength.",
                "Do not confuse DES expansion with AES MixColumns.",
            ],
        },
        "revise": {
            "bullets": [
                "64-bit Feistel cipher; 16 rounds; 56-bit effective key.",
                "IP → 16 rounds → FP; reverse keys to decrypt.",
                "S-boxes are the nonlinear core of f.",
                "Key schedule yields 48-bit subkeys.",
                "Historically broken mainly by short key length (see next topic).",
            ],
            "flash": [
                {"q": "DES block and key sizes?", "a": "64-bit block; 56-bit effective key (64 with parity)."},
                {"q": "How many DES rounds?", "a": "16 Feistel rounds."},
                {"q": "DES S-box size?", "a": "Each S-box maps 6 bits to 4 bits (eight S-boxes)."},
                {"q": "Decrypt DES?", "a": "Same algorithm with round keys K16…K1."},
            ],
        },
        "related": ["2.1.3", "2.1.5", "2.1.8"],
    }
)

add(
    {
        "id": "2.1.5",
        "title": "Strength of DES",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": False,
        "tags": ["brute-force", "weak-keys", "56-bit", "EFF-cracker", "3DES"],
        "learn": {
            "concept": (
                "DES strength debates split into algorithm-structure concerns and the 56-bit key length. "
                "Today the practical insecurity is exhaustive search on 2^56 keys — demonstrated by specialised "
                "hardware (EFF DES cracker, 1998, under three days) — not a collapse of the Feistel idea itself."
            ),
            "howItWorks": (
                "Key-length issue\n"
                "- ~7.2×10^16 keys; feasible for dedicated crackers and increasingly for commodity clusters.\n"
                "- Longer keys (e.g. move to AES-128) defeat pure brute force.\n\n"
                "Algorithmic concerns\n"
                "- Weak / semi-weak keys with pathological schedules — avoid them.\n"
                "- Complementary property used in some analyses.\n"
                "- Differential and linear cryptanalysis reduce complexity vs naive brute force but remain costly for full DES.\n"
                "- Oddities such as colliding S-box inputs; unclear crypto role of IP/FP.\n\n"
                "Migration path\n"
                "- 3DES extended DES hardware life; AES replaced DES for new designs."
            ),
            "example": (
                "Stem “why is DES insecure now?” → 56-bit exhaustive search is practical. Trap: claiming "
                "“Feistel is broken” or that differential cryptanalysis “breaks DES instantly.”"
            ),
            "compare": None,
            "remember": [
                "Main weakness today: 56-bit key space.",
                "EFF DES cracker showed practical brute force.",
                "Weak keys exist but are rare; examiners still love the term.",
                "Analytical attacks ≠ instant break of full DES.",
                "Security of DES ≠ security of a longer-key Feistel design.",
            ],
        },
        "revise": {
            "bullets": [
                "Two concern classes: algorithm quirks vs 56-bit key.",
                "2^56 is searchable with specialised hardware.",
                "Avoid weak/semi-weak keys.",
                "DC/LC matter historically but key length dominates practice.",
                "Replacements: 3DES (legacy), AES (modern).",
            ],
            "flash": [
                {"q": "Primary practical weakness of DES?", "a": "56-bit key enables exhaustive search."},
                {"q": "What did the 1998 EFF cracker show?", "a": "DES can be broken by dedicated brute-force hardware in days."},
                {"q": "Weak keys?", "a": "Pathological keys with poor key-schedule behaviour — must be avoided."},
                {"q": "Did Feistel fail?", "a": "No — short key length failed; Feistel structure remains a valid design pattern."},
            ],
        },
        "related": ["2.1.4", "2.1.6", "2.1.8", "2.2.1"],
    }
)

add(
    {
        "id": "2.1.6",
        "title": "Idea of Differential Cryptanalysis",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": False,
        "tags": ["differential", "ΔP", "characteristic", "S-box", "chosen-plaintext"],
        "learn": {
            "concept": (
                "Differential cryptanalysis studies how differences between plaintext pairs propagate to "
                "ciphertext differences. Biases in those difference distributions leak information about "
                "round keys and S-boxes. It is typically a chosen-plaintext style attack using many pairs."
            ),
            "howItWorks": (
                "Core idea\n"
                "- Choose ΔP = P ⊕ P′; encrypt both; observe ΔC = C ⊕ C′.\n"
                "- A characteristic is a predicted difference path through rounds with some probability.\n"
                "- Difference distribution tables summarise S-box behaviour under differentials.\n\n"
                "Why it matters for DES/AES history\n"
                "- DES S-boxes resist DC better than random boxes — design target (criteria once secret).\n"
                "- Related cousin: linear cryptanalysis uses linear approximations instead of differences.\n\n"
                "Not the same as\n"
                "- Traffic analysis, side-channel power analysis, or simple known-plaintext lookup."
            ),
            "example": (
                "Exam outline: “attacker chooses many plaintext pairs with fixed ΔP, collects ΔC statistics, "
                "matches likely characteristics, recovers key bits.” Mention probability of characteristics if asked."
            ),
            "compare": None,
            "remember": [
                "Stem “plaintext difference → ciphertext difference” → differential cryptanalysis.",
                "Usually needs many chosen pairs.",
                "Attacks nonlinear S-boxes via difference tables.",
                "DES S-boxes were tuned against DC.",
                "Do not confuse with side-channel or traffic analysis.",
            ],
        },
        "revise": {
            "bullets": [
                "Track ΔP through rounds to biased ΔC.",
                "Characteristics = probable difference paths.",
                "Chosen-plaintext flavour; lots of pairs.",
                "S-box DDT is the analytic engine.",
                "Linear cryptanalysis is the parallel approximation idea.",
            ],
            "flash": [
                {"q": "What does differential cryptanalysis study?", "a": "How plaintext differences propagate to ciphertext differences."},
                {"q": "What is a differential characteristic?", "a": "A predicted multi-round difference path with an associated probability."},
                {"q": "Typical attack model?", "a": "Chosen-plaintext (many structured pairs)."},
                {"q": "DC vs side-channel?", "a": "DC is algorithmic/statistical on input–output differences; side-channel uses physical leakage."},
            ],
        },
        "related": ["2.1.4", "2.1.5", "1.1.6"],
    }
)

add(
    {
        "id": "2.1.7",
        "title": "Block Cipher Modes of Operations",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": False,
        "tags": ["ECB", "CBC", "CFB", "OFB", "CTR"],
        "learn": {
            "concept": (
                "A block cipher encrypts one block; a mode of operation defines how to encrypt arbitrary-length "
                "messages. Mode ≠ algorithm: AES-CBC means the AES primitive used in CBC mode. Never use "
                "ECB for structured data."
            ),
            "howItWorks": (
                "ECB\n"
                "- Independent E_K(P_i). Identical plaintext blocks → identical ciphertext (pattern leak).\n\n"
                "CBC\n"
                "- C_i = E_K(P_i ⊕ C_{i−1}); C_0 from IV. Hides repeated blocks; sequential.\n\n"
                "CFB\n"
                "- Encrypt a shift register / IV, XOR with plaintext → ciphertext fed back (self-synchronising stream-like).\n\n"
                "OFB\n"
                "- Keystream from repeatedly encrypting the register; feedback is the cipher output, not ciphertext.\n"
                "- Keystream independent of plaintext.\n\n"
                "CTR\n"
                "- Encrypt nonce∥counter to make a keystream; highly parallel; never reuse counter under same key.\n\n"
                "IV / nonce\n"
                "- Uniqueness usually matters more than secrecy (mode-dependent)."
            ),
            "example": (
                "Encrypting a bitmap in ECB leaves the image outline visible in ciphertext. CBC with a random "
                "IV removes that cookie-cutter pattern. CTR with a reused nonce fails like a reused stream keystream."
            ),
            "compare": [
                {
                    "title": "ECB",
                    "bullets": [
                        "Independent blocks",
                        "Same P → same C",
                        "Parallel but insecure for structured data",
                    ],
                },
                {
                    "title": "CBC",
                    "bullets": [
                        "XOR with previous C (needs IV)",
                        "Hides repeated plaintext blocks",
                        "Sequential; padding-oracle risks in flawed stacks",
                    ],
                },
            ],
            "remember": [
                "Stem “same blocks look the same” → ECB weakness.",
                "Stem “XOR previous ciphertext” → CBC.",
                "OFB vs CFB: OFB feeds cipher output; CFB feeds ciphertext.",
                "CTR: parallel encrypt, but nonce/counter reuse is catastrophic.",
                "Mode is independent of whether the primitive is DES or AES.",
            ],
        },
        "revise": {
            "bullets": [
                "Modes stitch blocks into message encryption.",
                "ECB leaks patterns; avoid for real data.",
                "CBC needs IV; chains via previous ciphertext.",
                "CFB/OFB/CTR build stream-like encryption from a block cipher.",
                "Never reuse CTR nonce/counter under one key.",
            ],
            "flash": [
                {"q": "Why is ECB unsafe?", "a": "Identical plaintext blocks produce identical ciphertext blocks."},
                {"q": "CBC encryption formula?", "a": "C_i = E_K(P_i ⊕ C_{i−1}) with IV as C_0."},
                {"q": "CTR idea?", "a": "Encrypt a counter to get a keystream, XOR with plaintext."},
                {"q": "Mode vs algorithm?", "a": "Algorithm is the block primitive; mode defines multi-block usage."},
            ],
        },
        "related": ["1.1.8", "2.1.1", "2.1.4"],
    }
)

add(
    {
        "id": "2.1.8",
        "title": "Triple DES",
        "module": 2,
        "group": "Secret Key Cryptography",
        "lmr": False,
        "tags": ["3DES", "EDE", "two-key", "three-key", "meet-in-the-middle"],
        "learn": {
            "concept": (
                "Triple DES (3DES / TDEA) applies DES three times to lengthen effective keying without "
                "designing a new cipher. Standard form is EDE: encrypt–decrypt–encrypt. Block size remains "
                "64 bits, so birthday bounds still limit bulk use; AES is preferred for new systems."
            ),
            "howItWorks": (
                "Algorithm\n"
                "- Ciphertext = E_{K3}(D_{K2}(E_{K1}(P))).\n"
                "- Plaintext = D_{K1}(E_{K2}(D_{K3}(C))).\n\n"
                "Keying options (SLM)\n"
                "- Option 1: K1, K2, K3 independent (~168 key bits before MITM caveats).\n"
                "- Option 2: K3 = K1 (two-key 3DES, ~112-bit intent).\n"
                "- Option 3: K1 = K2 = K3 → collapses to single DES (legacy interop) — not recommended.\n\n"
                "Why EDE (middle decrypt)\n"
                "- Compatibility and strength properties when keys are related; middle decrypt is intentional.\n\n"
                "Security caveats\n"
                "- Meet-in-the-middle → effective security < naïve 3×56.\n"
                "- Still a 64-bit block cipher → volume limits; slower than AES."
            ),
            "example": (
                "Stem “encrypt, decrypt, encrypt with DES” → 3DES EDE. Trap: claiming three independent "
                "56-bit keys give 168-bit security against MITM, or that 3DES uses three different algorithms."
            ),
            "compare": None,
            "remember": [
                "3DES = three DES operations (usually EDE), not three algorithms.",
                "Two-key vs three-key keying options.",
                "K1=K2=K3 reduces to DES for backward compatibility.",
                "MITM reduces effective strength below 3×56.",
                "AES replaces 3DES for new designs; 64-bit block remains a limit.",
            ],
        },
        "revise": {
            "bullets": [
                "EDE: E_K1, D_K2, E_K3 on 64-bit blocks.",
                "Three keying options; option 1 strongest.",
                "Option 3 = single DES interop.",
                "MITM and 64-bit birthday bound matter.",
                "Legacy bridge toward AES.",
            ],
            "flash": [
                {"q": "3DES encryption formula?", "a": "C = E_K3(D_K2(E_K1(P)))."},
                {"q": "Two-key 3DES?", "a": "K3=K1 with independent K2 (~112-bit intended security, MITM caveats)."},
                {"q": "Why middle decrypt?", "a": "EDE form; enables DES compatibility when all keys equal."},
                {"q": "Why prefer AES over 3DES?", "a": "Faster, 128-bit block, stronger modern margins; 3DES is legacy."},
            ],
        },
        "related": ["2.1.4", "2.1.5", "2.2.1"],
    }
)

# ---------------------------------------------------------------------------
# Module 2 — Public key
# ---------------------------------------------------------------------------

add(
    {
        "id": "2.2.1",
        "title": "Advanced Encryption Standard (AES)",
        "module": 2,
        "group": "Public Key Cryptography",
        "lmr": False,
        "tags": ["AES", "Rijndael", "SubBytes", "MixColumns", "SPN"],
        "learn": {
            "concept": (
                "AES is the Rijndael-based NIST symmetric block cipher: 128-bit block; keys 128/192/256 "
                "bits map to 10/12/14 rounds. It is an SPN (not Feistel), faster and stronger than 3DES for "
                "modern use. Note: the curriculum groups AES under the public-key module heading, but AES "
                "itself is secret-key cryptography."
            ),
            "howItWorks": (
                "Round layers\n"
                "- SubBytes: nonlinear S-box (confusion).\n"
                "- ShiftRows: row-wise byte rotations (diffusion help).\n"
                "- MixColumns: column mixing over GF(2^8) (diffusion) — omitted in the final round.\n"
                "- AddRoundKey: XOR state with round key.\n\n"
                "Key expansion\n"
                "- Derive round keys from the cipher key.\n\n"
                "Decryption\n"
                "- Inverse layers in reverse order (unlike Feistel’s same-structure trick).\n\n"
                "Why it replaced DES/3DES\n"
                "- Larger keys/blocks, public competition winner, software-friendly, ~6× faster than 3DES in SLM claim."
            ),
            "example": (
                "Stem “128-bit block / SubBytes / MixColumns” → AES. Trap: listing DES IP/FP as AES steps, "
                "or saying “AES-128 means 128 rounds.”"
            ),
            "compare": [
                {
                    "title": "DES",
                    "bullets": [
                        "64-bit block, 56-bit key",
                        "16-round Feistel",
                        "Legacy; brute-forceable key",
                    ],
                },
                {
                    "title": "AES",
                    "bullets": [
                        "128-bit block; 128/192/256-bit keys",
                        "10/12/14-round SPN",
                        "Current standard for symmetric encryption",
                    ],
                },
            ],
            "remember": [
                "AES: 128-bit block; 10/12/14 rounds for 128/192/256-bit keys.",
                "Final round skips MixColumns.",
                "AES is SPN, not Feistel.",
                "SubBytes = confusion; ShiftRows/MixColumns = diffusion.",
                "AES-128 means 128-bit key (still 128-bit block).",
            ],
        },
        "revise": {
            "bullets": [
                "Rijndael SPN standardised as AES.",
                "Four layer types; MixColumns dropped in last round.",
                "Key expansion feeds AddRoundKey.",
                "Decrypt uses inverse operations, reverse order.",
                "Preferred replacement for DES/3DES.",
            ],
            "flash": [
                {"q": "AES block size?", "a": "Always 128 bits."},
                {"q": "Rounds for AES-128/192/256?", "a": "10, 12, and 14 rounds respectively."},
                {"q": "Which layer is skipped in the last round?", "a": "MixColumns."},
                {"q": "Is AES Feistel?", "a": "No — it is a substitution–permutation network."},
            ],
        },
        "related": ["2.1.2", "2.1.3", "2.1.8"],
    }
)

add(
    {
        "id": "2.2.2",
        "title": "Fermat’s and Euler’s Theorem",
        "module": 2,
        "group": "Public Key Cryptography",
        "lmr": False,
        "tags": ["Fermat", "Euler", "totient", "modular", "RSA-prep"],
        "learn": {
            "concept": (
                "Fermat’s Little Theorem and Euler’s theorem are the modular-arithmetic engines behind RSA "
                "correctness. Fermat is the prime-modulus special case of Euler. You will use φ(n) when "
                "choosing decryption exponents."
            ),
            "howItWorks": (
                "Fermat’s Little Theorem\n"
                "- If p is prime and gcd(a,p)=1, then a^(p−1) ≡ 1 (mod p).\n"
                "- Alternate form: a^p ≡ a (mod p) for prime p.\n\n"
                "Euler’s totient φ(n)\n"
                "- Count of integers in 1..n−1 coprime to n; φ(1)=1.\n"
                "- If p prime: φ(p)=p−1.\n"
                "- If n=pq distinct primes: φ(n)=(p−1)(q−1).\n\n"
                "Euler’s theorem\n"
                "- If gcd(a,n)=1, then a^φ(n) ≡ 1 (mod n).\n\n"
                "RSA link\n"
                "- Choose e with gcd(e, φ(n))=1; d ≡ e⁻¹ (mod φ(n)) so ed ≡ 1 (mod φ(n)).\n"
                "- Then M^(ed) ≡ M (mod n) under standard conditions."
            ),
            "example": (
                "Stem shows a^(p−1)≡1 mod p → Fermat. Stem shows a^φ(n)≡1 mod n → Euler. Trap: applying "
                "Fermat when the modulus is composite."
            ),
            "compare": [
                {
                    "title": "Fermat",
                    "bullets": [
                        "Modulus is prime p",
                        "a^(p−1) ≡ 1 (mod p) if p ∤ a",
                        "Special case of Euler (φ(p)=p−1)",
                    ],
                },
                {
                    "title": "Euler",
                    "bullets": [
                        "Modulus any n with gcd(a,n)=1",
                        "a^φ(n) ≡ 1 (mod n)",
                        "Directly used in RSA exponent setup",
                    ],
                },
            ],
            "remember": [
                "Fermat needs a prime modulus.",
                "Euler needs gcd(a,n)=1.",
                "φ(pq)=(p−1)(q−1) for distinct primes.",
                "RSA: ed ≡ 1 (mod φ(n)) (or mod λ(n) in modern statements).",
                "These theorems explain why decryption undoes encryption.",
            ],
        },
        "revise": {
            "bullets": [
                "Fermat: a^(p−1)≡1 mod p (p prime, p∤a).",
                "φ(n) counts residues coprime to n.",
                "Euler: a^φ(n)≡1 mod n when gcd(a,n)=1.",
                "Fermat ⊂ Euler for primes.",
                "RSA exponents are inverses mod φ(n).",
            ],
            "flash": [
                {"q": "State Fermat’s Little Theorem.", "a": "If p prime and gcd(a,p)=1 then a^(p−1)≡1 (mod p)."},
                {"q": "State Euler’s theorem.", "a": "If gcd(a,n)=1 then a^φ(n)≡1 (mod n)."},
                {"q": "φ(p) for prime p?", "a": "p−1."},
                {"q": "φ(pq) for distinct primes?", "a": "(p−1)(q−1)."},
            ],
        },
        "related": ["2.2.3", "2.2.5"],
    }
)

add(
    {
        "id": "2.2.3",
        "title": "Chinese Remainder Theorem",
        "module": 2,
        "group": "Public Key Cryptography",
        "lmr": False,
        "tags": ["CRT", "congruences", "coprime", "RSA-speedup"],
        "learn": {
            "concept": (
                "The Chinese Remainder Theorem (CRT) says a system x ≡ a_i (mod m_i) has a unique solution "
                "modulo M = ∏ m_i when the moduli are pairwise coprime. It is both an exam calculation tool "
                "and the standard speedup for RSA decryption (compute mod p and mod q, then combine)."
            ),
            "howItWorks": (
                "Constructive recipe (as in the SLM example)\n"
                "1. M = m1 m2 … mn.\n"
                "2. M_i = M / m_i.\n"
                "3. Find Z_i with M_i Z_i ≡ 1 (mod m_i).\n"
                "4. x = (∑ a_i Z_i M_i) mod M.\n\n"
                "Worked numbers from the SLM\n"
                "- x≡1 (mod 5), x≡1 (mod 7), x≡3 (mod 11) → M=385 → x=36.\n\n"
                "RSA use\n"
                "- Decrypt mod p and mod q separately (smaller exponents), CRT-combine to mod n.\n"
                "- Optimisation — not a different cryptosystem.\n\n"
                "If moduli are not coprime, uniqueness/solvability needs extra conditions."
            ),
            "example": (
                "Be ready for a tiny numeric CRT (two or three congruences). Also state: “RSA CRT decryption "
                "is faster modular arithmetic, same public key (n,e).”"
            ),
            "compare": None,
            "remember": [
                "Pairwise coprime moduli → unique solution mod product.",
                "Recipe: M, M_i, inverses Z_i, sum a_i Z_i M_i.",
                "RSA uses CRT as a decryption speedup.",
                "Forgetting the coprime hypothesis is the common trap.",
                "CRT combines residues; it does not invent a new public-key scheme.",
            ],
        },
        "revise": {
            "bullets": [
                "Solve simultaneous congruences when moduli are coprime.",
                "Unique answer modulo the product M.",
                "Standard sum-of-terms construction.",
                "RSA: decrypt mod p,q then CRT.",
                "Non-coprime moduli change the theorem’s guarantees.",
            ],
            "flash": [
                {"q": "CRT uniqueness condition?", "a": "Moduli pairwise coprime → unique solution mod their product."},
                {"q": "Role of M_i?", "a": "M_i = M/m_i; used with its inverse mod m_i in the constructive sum."},
                {"q": "SLM triple example result?", "a": "x≡1 mod 5, 1 mod 7, 3 mod 11 → x=36 mod 385."},
                {"q": "CRT in RSA?", "a": "Speed up private-key exponentiation via mod-p and mod-q then combine."},
            ],
        },
        "related": ["2.2.2", "2.2.5"],
    }
)

add(
    {
        "id": "2.2.4",
        "title": "Principals of Public Key Crypto Systems",
        "module": 2,
        "group": "Public Key Cryptography",
        "lmr": False,
        "tags": ["asymmetric", "public-key", "private-key", "hybrid", "trapdoor"],
        "learn": {
            "concept": (
                "Public-key (asymmetric) cryptography uses a related key pair: a public key anyone may use "
                "to encrypt or verify, and a private key kept secret for decrypt or sign. Security rests on "
                "trapdoor one-way functions (factoring, discrete log), not on hiding the public key."
            ),
            "howItWorks": (
                "Core principles (SLM list condensed)\n"
                "- Key pairs: public ↔ private mathematically linked; private not feasibly derived from public.\n"
                "- Confidentiality: encrypt with recipient’s public key; only their private key decrypts.\n"
                "- Signatures: sign with sender’s private key; verify with sender’s public key.\n"
                "- Authentication / challenge-response using private-key proofs.\n"
                "- Key exchange (e.g. Diffie–Hellman) builds shared secrets over open channels.\n\n"
                "Practice\n"
                "- Public-key ops are slow → hybrid encryption: wrap an AES session key with RSA/ECC, bulk-encrypt with AES.\n"
                "- Trust in public keys needs PKI or web-of-trust (later modules)."
            ),
            "example": (
                "Trap stem: “encrypt with private key for secrecy” — that is signing territory, not confidentiality. "
                "For secrecy, encrypt with the recipient’s public key."
            ),
            "compare": [
                {
                    "title": "Symmetric (secret key)",
                    "bullets": [
                        "Same key encrypts and decrypts",
                        "Fast; needs prior shared secret",
                        "Examples: DES, AES, 3DES",
                    ],
                },
                {
                    "title": "Public-key (asymmetric)",
                    "bullets": [
                        "Public encrypt/verify; private decrypt/sign",
                        "Solves key distribution; slower ops",
                        "Examples: RSA; DH for key agreement",
                    ],
                },
            ],
            "remember": [
                "Two keys: public shareable, private secret.",
                "Encrypt-to-recipient uses their public key.",
                "Sign-as-sender uses your private key.",
                "Hybrid encryption is how real systems move bulk data.",
                "Hard problems (factoring/DL) underpin security — public key is not secret.",
            ],
        },
        "revise": {
            "bullets": [
                "Asymmetric = public/private pair + trapdoor function.",
                "Confidentiality vs authenticity use opposite keys.",
                "Diffie–Hellman agrees keys; RSA can encrypt/sign.",
                "Always hybridise with a symmetric cipher for bulk data.",
                "PKI binds identities to public keys.",
            ],
            "flash": [
                {"q": "Public vs private key roles?", "a": "Public: encrypt/verify; private: decrypt/sign."},
                {"q": "Why hybrid encryption?", "a": "Public-key is slow — use it to protect a fast symmetric session key."},
                {"q": "Trapdoor one-way function?", "a": "Easy forward; hard to invert without the trapdoor (private key)."},
                {"q": "Encrypt with private key?", "a": "That produces a signature-like proof, not confidential ciphertext."},
            ],
        },
        "related": ["2.1.1", "2.2.5", "2.2.6"],
    }
)

add(
    {
        "id": "2.2.5",
        "title": "RSA Algorithm",
        "module": 2,
        "group": "Public Key Cryptography",
        "lmr": False,
        "tags": ["RSA", "modulus", "exponent", "encrypt", "sign"],
        "learn": {
            "concept": (
                "RSA (Rivest–Shamir–Adleman) is the classic public-key cryptosystem based on modular "
                "exponentiation and the hardness of factoring n = pq. Public key (n, e); private exponent d "
                "(and usually p, q). Correctness follows from Euler/Fermat once ed ≡ 1 (mod φ(n))."
            ),
            "howItWorks": (
                "Key generation\n"
                "1. Choose large secret primes p, q; n = pq.\n"
                "2. φ(n) = (p−1)(q−1).\n"
                "3. Pick e with gcd(e, φ(n))=1 (often 65537).\n"
                "4. d ≡ e⁻¹ (mod φ(n)).\n"
                "5. Publish (n, e); keep d (and p, q) private.\n\n"
                "Encrypt / decrypt\n"
                "- C = M^e mod n (0 < M < n, with padding in practice).\n"
                "- M = C^d mod n.\n\n"
                "Signing variant\n"
                "- Sign with d; verify with e — same maths, authenticity goal.\n\n"
                "Practice warning\n"
                "- Textbook/raw RSA is malleable; use padding (OAEP, etc.)."
            ),
            "example": (
                "Tiny teaching numbers (not secure): p=3, q=11, n=33, φ=20, e=3, d=7. "
                "M=4 → C=4^3 mod 33=31 → 31^7 mod 33=4."
            ),
            "compare": None,
            "remember": [
                "Setup: n=pq; ed≡1 mod φ(n); C=M^e mod n; M=C^d mod n.",
                "n and e are public; p, q, d stay secret.",
                "Factoring n yields φ(n) and thus d.",
                "Message must be encoded as an integer in range (with padding).",
                "Signing uses private exponent; encryption uses public exponent.",
            ],
        },
        "revise": {
            "bullets": [
                "RSA keygen from two primes and inverse exponents.",
                "Encrypt with e; decrypt with d (mod n).",
                "Correctness from Euler/Fermat.",
                "Same maths supports signatures.",
                "Always pad in real deployments.",
            ],
            "flash": [
                {"q": "RSA public key?", "a": "(n, e) with n=pq and gcd(e, φ(n))=1."},
                {"q": "RSA encryption?", "a": "C = M^e mod n."},
                {"q": "RSA decryption?", "a": "M = C^d mod n where d = e⁻¹ mod φ(n)."},
                {"q": "Why keep p and q secret?", "a": "Knowing factors gives φ(n) and recovers d."},
            ],
        },
        "related": ["2.2.2", "2.2.3", "2.2.4", "2.2.6"],
    }
)

add(
    {
        "id": "2.2.6",
        "title": "Security of RSA Algorithm",
        "module": 2,
        "group": "Public Key Cryptography",
        "lmr": False,
        "tags": ["factoring", "padding", "Wiener", "side-channel", "key-size"],
        "learn": {
            "concept": (
                "RSA security, under good parameters, rests on the hardness of factoring n (and related RSA "
                "problems). If p and q are known, φ(n) and d follow and the scheme collapses. In practice, "
                "bad parameters and bad implementations fail long before asymptotic factoring breakthroughs."
            ),
            "howItWorks": (
                "Main threats\n"
                "- Factoring n → compute φ → invert e to get d.\n"
                "- Small/exponent attacks: tiny e with small M; Wiener’s attack on small d.\n"
                "- Common modulus: same n with different e’s for one M can leak the message.\n"
                "- Padding omission: textbook RSA is malleable and vulnerable to many practical attacks.\n"
                "- Side-channels: timing/power on modular exponentiation leak d.\n\n"
                "Operational controls\n"
                "- Use large keys (historically 1024 → 2048+ bits) and vetted libraries.\n"
                "- Hybrid use still needs strong RSA parameters on the key wrap.\n"
                "- Quantum note: Shor’s algorithm threatens factoring/DL schemes — RSA is not quantum-safe."
            ),
            "example": (
                "Stem “why RSA fails if p,q known” → compute φ(n)=(p−1)(q−1), then d = e⁻¹ mod φ(n). "
                "Trap: “RSA is secure because e is secret” — e is public."
            ),
            "compare": None,
            "remember": [
                "Factoring n breaks RSA.",
                "e is public — secrecy of e is never the claim.",
                "Pad messages; avoid tiny d / reckless e+M choices.",
                "Implementation bugs and side-channels often kill RSA first.",
                "Grow key sizes over time; plan post-quantum migration separately.",
            ],
        },
        "revise": {
            "bullets": [
                "Hardness ≈ factoring n under sound parameters.",
                "p,q known ⇒ φ known ⇒ d known.",
                "Small-d / small-e / common-modulus are classic pitfalls.",
                "Padding is mandatory in practice.",
                "Side-channels and bad RNGs beat textbook security claims.",
            ],
            "flash": [
                {"q": "What happens if n is factored?", "a": "Attacker computes φ(n) and recovers d — RSA is broken."},
                {"q": "Is e secret?", "a": "No — the public exponent is published with n."},
                {"q": "Why padding?", "a": "Raw RSA is malleable and open to several practical attacks."},
                {"q": "Side-channel risk?", "a": "Timing/power traces during exponentiation can leak d."},
            ],
        },
        "related": ["2.2.4", "2.2.5", "1.1.9"],
    }
)


def main() -> None:
    assert len(CONCEPTS) == 23, len(CONCEPTS)
    expected = (
        [f"1.1.{i}" for i in range(1, 10)]
        + [f"2.1.{i}" for i in range(1, 9)]
        + [f"2.2.{i}" for i in range(1, 7)]
    )
    assert list(CONCEPTS.keys()) == expected, set(expected) - set(CONCEPTS)

    # Feistel spelling check
    blob = json.dumps(CONCEPTS)
    assert "Fiestal" not in blob and "fiestal" not in blob
    assert "Feistel" in blob

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps({"concepts": CONCEPTS}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(CONCEPTS)} concepts to {OUT}")


if __name__ == "__main__":
    main()
