# 🔐 PKI + TOTP Authentication Microservice

## 📌 Overview

This project implements a **secure, containerized authentication microservice** that demonstrates enterprise-grade security practices using:

* **Public Key Infrastructure (PKI)** with RSA-4096
* **Time-based One-Time Password (TOTP)** based 2FA
* **Dockerized deployment** with persistent storage
* **Cron job execution** inside a container

The service securely decrypts an instructor-provided seed, generates TOTP codes, verifies them with time tolerance, and logs 2FA codes every minute using cron.

---

## 🛠️ Tech Stack

* **Language**: Python 3
* **Framework**: FastAPI
* **Cryptography**: `cryptography` (RSA-OAEP, RSA-PSS)
* **TOTP**: `pyotp`
* **Containerization**: Docker, Docker Compose
* **Scheduling**: cron (inside Docker)

---

## 🔐 Cryptographic Details

* **RSA Key Size**: 4096 bits
* **Public Exponent**: 65537
* **Seed Decryption**: RSA-OAEP with SHA-256 + MGF1
* **Commit Proof**: RSA-PSS with SHA-256 (max salt length)
* **TOTP Algorithm**: SHA-1
* **TOTP Period**: 30 seconds
* **Digits**: 6

---

## 📂 Project Structure

```
.
├── app/
│   └── main.py                 # FastAPI application
├── scripts/
│   └── log_2fa_cron.py          # Cron script for logging 2FA codes
├── cron/
│   └── 2fa-cron                 # Cron configuration (LF endings)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── student_private.pem          # Student RSA private key (assignment-only)
├── student_public.pem           # Student RSA public key
├── instructor_public.pem        # Instructor public key
├── .gitignore
├── .gitattributes
└── README.md
```

> ⚠️ `encrypted_seed.txt` is **NOT committed** (intentionally gitignored).

---

## 🚀 API Endpoints

### 1️⃣ POST `/decrypt-seed`

Decrypts the instructor-provided encrypted seed and stores it persistently.

**Request**

```json
{
  "encrypted_seed": "BASE64_ENCRYPTED_SEED"
}
```

**Response**

```json
{
  "status": "ok"
}
```

* Stores decrypted seed at `/data/seed.txt`
* Uses RSA-OAEP with SHA-256

---

### 2️⃣ GET `/generate-2fa`

Generates the current TOTP code.

**Response**

```json
{
  "code": "123456",
  "valid_for": 30
}
```

* Reads seed from `/data/seed.txt`
* Converts hex seed → base32
* Uses SHA-1, 30s period, 6 digits

---

### 3️⃣ POST `/verify-2fa`

Verifies a submitted TOTP code with time tolerance.

**Request**

```json
{
  "code": "123456"
}
```

**Response**

```json
{
  "valid": true
}
```

* Allows ±1 time window (±30 seconds)

---

## ⏱️ Cron Job

* Runs **every minute**
* Reads seed from `/data/seed.txt`
* Generates current TOTP code
* Logs output to `/cron/last_code.txt`

**Log Format**

```
YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX
```

* Timezone: **UTC**
* Cron file uses **LF (Unix) line endings**

---

## 🐳 Docker Setup

### Build & Run

```bash
docker-compose build
docker-compose up -d
```

* API exposed on **port 8080**
* Cron runs in foreground
* Volumes ensure persistence

### Volumes

* `/data` → stores decrypted seed (`seed.txt`)
* `/cron` → stores cron output (`last_code.txt`)

---

## 🔁 Persistence Test

Seed persists across container restarts:

```bash
docker-compose down
docker-compose up -d
```

```bash
docker exec pki-totp-auth ls /data
```

Expected:

```
seed.txt
```

---

## 🔐 Commit Proof (Submission Requirement)

* Commit hash is signed using **RSA-PSS (SHA-256)**
* Signature encrypted using **Instructor Public Key (RSA-OAEP)**
* Final output is **base64-encoded single-line string**

---

## ⚠️ Security Notice

* RSA keys committed **only for this assignment**
* Keys are **NOT reused** for any real-world purpose
* Consider keys compromised after submission

---

## ✅ Submission Checklist

* Public GitHub repository
* Correct repository URL (matches instructor API request)
* All APIs functional
* Docker container builds and runs
* Seed persists after restart
* Cron job configured correctly
* Commit proof generated correctly

---

## 👩‍💻 Author

**Swetha**
B.Tech – Computer Science
Project: *Secure PKI + TOTP Authentication Microservice*

---
