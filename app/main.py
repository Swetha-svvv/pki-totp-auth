from fastapi import FastAPI, HTTPException
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import base64
import os
import pyotp
import time

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
PRIVATE_KEY_PATH = BASE_DIR / "student_private.pem"

DATA_DIR = Path("/data")
SEED_FILE = DATA_DIR / "seed.txt"


def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )


def decrypt_seed_b64(encrypted_b64: str) -> str:
    private_key = load_private_key()
    encrypted_bytes = base64.b64decode(encrypted_b64)
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    seed = decrypted.decode("utf-8")
    if len(seed) != 64:
        raise ValueError("Invalid seed length")
    return seed


def get_totp(hex_seed: str) -> pyotp.TOTP:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")
    return pyotp.TOTP(base32_seed)


@app.post("/decrypt-seed")
def decrypt_seed_api(payload: dict):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        encrypted_seed = payload.get("encrypted_seed")
        if not encrypted_seed:
            raise HTTPException(status_code=400, detail="Missing encrypted_seed")
        seed = decrypt_seed_b64(encrypted_seed)
        SEED_FILE.write_text(seed)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    seed = SEED_FILE.read_text().strip()
    totp = get_totp(seed)
    code = totp.now()
    valid_for = 30 - (int(time.time()) % 30)
    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(payload: dict):
    if "code" not in payload:
        raise HTTPException(status_code=400, detail="Missing code")
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    code = payload["code"]
    seed = SEED_FILE.read_text().strip()
    totp = get_totp(seed)

    is_valid = totp.verify(code, valid_window=1)  # ±30 seconds
    return {"valid": bool(is_valid)}


@app.get("/")
def health():
    return {"status": "ok"}
