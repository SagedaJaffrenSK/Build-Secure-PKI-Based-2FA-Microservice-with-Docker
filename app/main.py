# app/scripts/main.py
from fastapi import FastAPI, HTTPException
import uvicorn
from pathlib import Path
from scripts.crypto_utils import decrypt_signature
from scripts.totp_utils import generate_secret_uri, verify_token

app = FastAPI()

@app.post("/decrypt-seed")
async def decrypt_seed(payload: dict):
    sig = payload.get("signature")
    if not sig:
        raise HTTPException(status_code=400, detail="signature required")
    seed_hex = decrypt_signature(sig)
    Path("/data").mkdir(parents=True, exist_ok=True)
    (Path("/data") / "seed.txt").write_text(seed_hex)
    return {"seed": seed_hex}

@app.get("/generate-2fa")
async def gen():
    secret, uri = generate_secret_uri("student")
    return {"secret": secret, "uri": uri}

@app.post("/verify-2fa")
async def verify(payload: dict):
    secret = payload.get("secret")
    token = payload.get("token")
    if not secret or not token:
        raise HTTPException(status_code=400, detail="secret & token required")
    ok = verify_token(secret, token)
    return {"valid": bool(ok)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
