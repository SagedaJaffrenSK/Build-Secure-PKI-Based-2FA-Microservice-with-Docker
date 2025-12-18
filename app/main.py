# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from app.crypto_utils import decrypt_signature
from app.totp_utils import generate_secret_uri, verify_token

app = FastAPI()

SEED_PATH = "/data/seed.txt"


class EncryptedSeed(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    token: str


# ------------------ DECRYPT SEED ------------------
@app.post("/decrypt-seed")
def decrypt_seed(payload: EncryptedSeed):
    try:
        secret = decrypt_signature(payload.encrypted_seed)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(secret)

        return {"message": "Seed decrypted and stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------ GENERATE 2FA ------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=400, detail="Seed not found")

    with open(SEED_PATH, "r") as f:
        secret = f.read().strip()

    _, uri = generate_secret_uri()
    return {"provisioning_uri": uri}


# ------------------ VERIFY 2FA ------------------
@app.post("/verify-2fa")
def verify_2fa(data: VerifyRequest):
    if not os.path.exists(SEED_PATH):
        raise HTTPException(status_code=400, detail="Seed not found")

    with open(SEED_PATH, "r") as f:
        secret = f.read().strip()

    if verify_token(secret, data.token):
        return {"status": "success"}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
