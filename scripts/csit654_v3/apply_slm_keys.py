"""Apply SLM/PDF-grounded answers onto Amigo topic scrapes; keep amigo_review when present."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOPIC = ROOT / "subjects" / "csit654" / "v3" / "source" / "amigo" / "topic"
KEYS_OUT = ROOT / "subjects" / "csit654" / "v3" / "source" / "amigo" / "_slm_keys.json"

# (cmid, no) -> (correct_index, short explanation)
SLM: dict[tuple[str, str], tuple[int, str]] = {
    ("326318", "1"): (1, "Active attacks involve intentional modification/disruption (malicious intent)."),
    ("326318", "2"): (0, "DoS is a classic class of computer/network threat in the SLM."),
    ("326320", "1"): (2, "Authorization decides user rights/privileges after authentication."),
    ("326320", "2"): (1, "Digital signatures primarily support integrity (and authenticity/non-repudiation)."),
    ("326322", "1"): (1, "Asymmetric crypto uses a public/private key pair."),
    ("326322", "2"): (0, "Symmetric crypto uses the same shared secret to lock and unlock."),
    ("326324", "1"): (3, "Drill cipher is not a standard classical/conventional technique in the SLM set."),
    ("326324", "2"): (1, "Transposition ciphers rearrange (shuffle) letter positions."),
    ("326326", "1"): (0, "Hill cipher is a substitution (polygraphic) cipher, not a transposition rail technique."),
    ("326326", "2"): (2, "One-time pad is a substitution stream scheme, not a transposition cipher."),
    ("326328", "1"): (0, "Trying every key/combination is a brute-force attack."),
    ("326328", "2"): (0, "Cryptanalysis seeks weaknesses in cryptographic schemes."),
    ("326330", "1"): (2, "Invisible ink (e.g., lime water) is a classical steganography technique."),
    ("326330", "2"): (1, "Steganography hides existence of data and can complement cryptography."),
    ("326332", "1"): (2, "Invisible ink / lime water steganography (same SLM point as 1.1.7)."),
    ("326332", "2"): (2, "Block ciphers are characterized by avalanche effect and completeness vs stream ciphers."),
    ("326334", "1"): (1, "Hardware compromise/piracy recovery is especially hard once devices are cloned/extracted."),
    ("326334", "2"): (3, "Antivirus software detects and helps avoid viruses/malware."),
    ("326339", "1"): (1, "Cipher strength is driven primarily by key length (Kerckhoffs/SLM emphasis)."),
    ("326339", "2"): (3, "ECB, CBC, and CTR are standard block-cipher modes of operation."),
    ("326341", "1"): (2, "Shannon confusion obscures the ciphertext–key relationship."),
    ("326341", "2"): (1, "False: ciphertext–plaintext hiding is diffusion; confusion targets the key relationship."),
    ("326343", "1"): (0, "Feistel structure is designed to build cryptographic complexity via rounds."),
    ("326343", "2"): (2, "Feistel does not require converting plaintext into a matrix first."),
    ("326345", "1"): (1, "DES performs 16 rounds of substitution/permutation operations."),
    ("326345", "2"): (1, "The heart of DES is its round structure."),
    ("326347", "1"): (2, "DES strength depends on the encryption key size/space."),
    ("326347", "2"): (2, "DES uses a 64-bit key block (56 effective + parity)."),
    ("326349", "1"): (1, "Differential cryptanalysis studies plaintext pairs and corresponding ciphertexts."),
    ("326349", "2"): (3, "Differential techniques apply across block ciphers, streams, and hash constructions."),
    ("326351", "1"): (3, "CTR mode encrypts a counter (then XOR with plaintext)."),
    ("326351", "2"): (3, "ECB has no chaining; a bit error can corrupt an entire independent block (worst isolation/propagation trade-off in classic MCQs)."),
    ("326353", "1"): (2, "Triple DES applies DES three times (EDE)."),
    ("326353", "2"): (1, "Common 2-key Triple-DES (EDE2) uses two keys; SLM lists two-key form."),
    ("326356", "1"): (2, "AES provides stronger modern security than DES/3DES."),
    ("326356", "2"): (2, "AES-256 uses 14 rounds."),
    ("326358", "1"): (3, "Fermat/Euler theorems are stated for (modular) prime-related arithmetic."),
    ("326358", "2"): (1, "The given polynomial claim is not a valid Euler-theorem identity as stated."),
    ("326360", "1"): (3, "CRT is applied with pairwise coprime / prime-power moduli in crypto settings."),
    ("326360", "2"): (0, "Cardinality of set S is commonly denoted #S."),
    ("326362", "1"): (1, "Public-key cryptography uses two keys (public and private)."),
    ("326362", "2"): (1, "Encryption and decryption use different keys in public-key systems."),
    ("326364", "1"): (3, "RSA is built on large prime numbers and modular exponentiation."),
    ("326364", "2"): (3, "RSA encrypts with the public key and decrypts with the private key."),
    ("326366", "1"): (0, "Exhaustive key search against RSA is a brute-force style attack."),
    ("326366", "2"): (1, "False: RSA is much slower/bulk-inefficient compared with DES/AES for bulk data."),
    ("326371", "1"): (0, "Message authentication verifies integrity and authenticity of messages."),
    ("326371", "2"): (0, "Authentication binds the claimed sender identity to the message."),
    ("326373", "1"): (2, "Hash/authentication functions map arbitrary messages to fixed-length authenticators."),
    ("326373", "2"): (3, "Correct relation is h=H(M); none of the listed formulas match cleanly."),
    ("326375", "1"): (1, "Observing communication patterns is traffic analysis."),
    ("326375", "2"): (0, "Source repudiation is denial of having sent a message."),
    ("326377", "1"): (3, "A MAC is a cryptographic checksum authenticating a message."),
    ("326377", "2"): (0, "MAC function C produces a cryptographic checksum on message M."),
    ("326379", "1"): (4, "SHA family includes SHA-0/1/2/3 variants covered in the material."),
    ("326379", "2"): (3, "SHA-1 input limit is < 2^64 bits; listed sizes are digest lengths, not the max input."),
    ("326381", "1"): (2, "A message digest is produced by a hash function."),
    ("326381", "2"): (0, "MD5 uses 4 rounds of 16 steps each."),
    ("326384", "1"): (1, "Digital signatures rely on asymmetric cryptography."),
    ("326384", "2"): (2, "A digital signature is the electronic counterpart of a handwritten signature."),
    ("326386", "1"): (0, "DSS = Digital Signature Standard."),
    ("326386", "2"): (1, "DSS is realized by the Digital Signature Algorithm (DSA)."),
    ("326389", "1"): (3, "Signatures support authenticity, integrity, and non-repudiation."),
    ("326389", "2"): (0, "Authentication verifies a user’s claimed identity."),
    ("326394", "1"): (0, "Kerberos is a network authentication protocol."),
    ("326394", "2"): (1, "Kerberos was developed at MIT."),
    ("326396", "1"): (2, "ACLs grant or deny access."),
    ("326396", "2"): (3, "ACL entries commonly match address, port, and protocol fields."),
    ("326398", "1"): (0, "PGP was created by Phil Zimmermann."),
    ("326398", "2"): (2, "PGP is an e-mail (and file) encryption system."),
    ("326400", "1"): (0, "S/MIME = Secure/Multipurpose Internet Mail Extensions."),
    ("326400", "2"): (1, "S/MIME extends MIME for secure mail."),
    ("326403", "1"): (2, "IPsec secures IP-layer communications."),
    ("326403", "2"): (3, "IPsec can protect host–host, network–network, and mixed paths."),
    ("326405", "1"): (1, "SSL/TLS provides end-to-end security over TCP."),
    ("326405", "2"): (0, "SSL was originally developed by Netscape."),
    ("326407", "1"): (3, "SET was jointly developed by Visa and Mastercard."),
    ("326407", "2"): (1, "SET secured online card payment transactions."),
    ("326412", "1"): (3, "Intrusion attempts may access, manipulate, or disrupt systems."),
    ("326412", "2"): (1, "Break-ins are detected via anomalous profiles / policy violations."),
    ("326414", "1"): (1, "IDS monitors for malicious activity."),
    ("326414", "2"): (2, "IDPS combines detection and prevention capabilities."),
    ("326416", "1"): (2, "Malware damages software/data (not typically physical hardware)."),
    ("326416", "2"): (1, "A virus inserts into and becomes part of another program."),
    ("326418", "1"): (3, "Network firewalls operate across multiple layers with varied criteria."),
    ("326418", "2"): (3, "Stateful multilayer inspection generally provides the strongest classic firewall model."),
    ("326420", "1"): (0, "IT Act 2000 came into force on 17 October 2000."),
    ("326420", "2"): (3, "IT Act covers e-documents, digital signatures, and offences."),
    ("326422", "1"): (1, "VPNs protect against unauthorized eavesdropping."),
    ("326422", "2"): (1, "VPN tunneling encapsulates packets (e.g., in IP)."),
    ("326424", "1"): (0, "A packet analyzer/sniffer captures and inspects traffic."),
    ("326424", "2"): (1, "Buffer overflow occurs when data exceeds buffer capacity."),
    ("326426", "1"): (1, "Blockchain records information in linked blocks that resist alteration."),
    ("326426", "2"): (3, "Each block references the previous block in the chain."),
    ("326428", "1"): (1, "Piracy is unauthorized copying/use of copyrighted material."),
    ("326428", "2"): (0, "Privacy is freedom from unwanted public scrutiny/disclosure."),
    ("326431", "1"): (2, "Forensic acquisition uses both hardware and software tools."),
    ("326431", "2"): (3, "EnCase/FTK/TSK are not China-origin tools; answer is none of these as ‘Chinese-made’."),
    ("326433", "1"): (4, "Forensic process: identify, acquire, analyze, report."),
    ("326433", "2"): (0, "Establishing/identifying the scene dimensions is a critical first CSI step."),
    ("326436", "1"): (4, "Cyber forensics identifies, collects, preserves, and analyzes data."),
    ("326436", "2"): (4, "Forensics supports controls, reporting, compliance, and fraud detection."),
    ("326438", "1"): (2, "Both hardware and software forensic tools gather evidence."),
    ("326438", "2"): (3, "Listed tools are not China-made; select none of these."),
    ("326440", "1"): (4, "Digital forensics covers computers, phones, servers, and networks."),
    ("326440", "2"): (1, "Digital evidence comes from electronic devices."),
    ("326442", "1"): (2, "OS forensics retrieves artifacts from the operating system."),
    ("326442", "2"): (0, "TCPView shows network connections/associations."),
    ("326444", "1"): (3, "Email tracing helps investigate spoofing, phishing, and online frauds."),
    ("326444", "2"): (2, "Email tracing/tracking monitors e-mail delivery."),
}


def main():
    key_questions = []
    patched = 0
    for path in sorted(TOPIC.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        cmid = str(data.get("cmid") or path.stem)
        changed = False
        for q in data.get("questions") or []:
            no = str(q.get("no") or "")
            if q.get("correct") is not None and q.get("answerSource") == "amigo_review":
                key_questions.append(
                    {
                        "id": f"amigo-t-{cmid}-{no}",
                        "correct": q["correct"],
                        "explanation": q.get("explanation") or "",
                        "answerSource": "amigo_review",
                    }
                )
                continue
            if (cmid, no) in SLM:
                correct, expl = SLM[(cmid, no)]
                q["correct"] = correct
                q["answerSource"] = "slm"
                q["explanation"] = expl
                changed = True
                key_questions.append(
                    {
                        "id": f"amigo-t-{cmid}-{no}",
                        "correct": correct,
                        "explanation": expl,
                        "answerSource": "slm",
                    }
                )
            elif q.get("correct") is not None:
                q["answerSource"] = q.get("answerSource") or "amigo_review"
                key_questions.append(
                    {
                        "id": f"amigo-t-{cmid}-{no}",
                        "correct": q["correct"],
                        "explanation": q.get("explanation") or "",
                        "answerSource": q["answerSource"],
                    }
                )
        if changed:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            patched += 1
    KEYS_OUT.write_text(
        json.dumps({"questions": key_questions}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"patched_files={patched} key_entries={len(key_questions)}")


if __name__ == "__main__":
    main()
