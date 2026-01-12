#!/usr/bin/env python3

import base64
import pyotp
from pathlib import Path
from datetime import datetime, timezone

SEED_FILE = Path("/data/seed.txt")
CRON_OUTPUT = Path("/cron/last_code.txt")


def generate_totp(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode("utf-8")
    totp = pyotp.TOTP(base32_seed)
    return totp.now()


def main():
    if not SEED_FILE.exists():
        print("Seed file not found")
        return

    seed = SEED_FILE.read_text().strip()
    code = generate_totp(seed)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}")


if __name__ == "__main__":
    main()
