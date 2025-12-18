#!/usr/bin/env python3
import sys
import subprocess
import base64
import hashlib
from pathlib import Path

# --- Absolute paths to PEM files ---
base_dir = Path(__file__).resolve().parent.parent  # project root
priv_path = base_dir / "student_private.pem"
instr_pub_path = base_dir / "instructor_public.pem"

# --- Add project root to Python path to import crypto_utils ---
sys.path.append(str(base_dir))
from crypto_utils import rsa_pss_sign, rsa_oaep_encrypt

# --- Read PEM files ---
priv = priv_path.read_bytes()
instr_pub = instr_pub_path.read_bytes()

# --- Get latest commit hash ---
commit_hash = subprocess.check_output(["git", "log", "-1", "--format=%H"]).decode().strip()
print("Commit Hash:", commit_hash)

# --- Sign the commit hash ---
signature = rsa_pss_sign(commit_hash.encode("utf-8"), priv)

# --- Encrypt a SHA-256 digest of the commit hash with instructor public key ---
commit_digest = hashlib.sha256(commit_hash.encode("utf-8")).digest()
enc_sig = rsa_oaep_encrypt(commit_digest, instr_pub)

# --- Output base64 ---
b64 = base64.b64encode(enc_sig).decode("utf-8")
print("Encrypted Signature (base64, single line):")
print(b64)
