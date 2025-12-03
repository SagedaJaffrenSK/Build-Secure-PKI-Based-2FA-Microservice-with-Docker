import os, base64, time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import pyotp
from .crypto_utils import rsa_oaep_decrypt

app = FastAPI()

DATA_DIR = Path("/data")
SEED_FILE = DATA_DIR / "seed.txt"
DATA_DIR.mkdir(parents=True, exist_ok=True)

class DecryptRequest(BaseModel):
    encrypted_seed: str

@app.post("/decrypt-seed")
async def decrypt_seed(req: DecryptRequest):
    try:
        with open("/app/student_private.pem", "rb") as f:
            priv_pem = f.read()
        seed = rsa_oaep_decrypt(req.encrypted_seed, priv_pem)
        SEED_FILE.write_text(seed)
        os.chmod(SEED_FILE, 0o600)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail={"error": "Decryption failed"})

@app.get("/generate-2fa")
async def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    hex_seed = SEED_FILE.read_text().strip()
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    code = totp.now()
    period_elapsed = int(time.time()) % 30
    valid_for = 30 - period_elapsed
    return {"code": code, "valid_for": valid_for}

class VerifyRequest(BaseModel):
    code: str

@app.post("/verify-2fa")
async def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
    hex_seed = SEED_FILE.read_text().strip()
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    is_valid = totp.verify(req.code, valid_window=1)
    return {"valid": bool(is_valid)}

@app.get("/health")
async def health():
    return {"status": "ok"}
