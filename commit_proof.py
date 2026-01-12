import base64
from cryptography.hazmat.primitives import serialization
from crypto_utils import rsa_sign_pss_sha256
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes


def load_private_key(path="student_private.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None)


def load_instructor_public_key(path="instructor_public.pem"):
    with open(path, "rb") as f:
        return serialization.load_pem_public_key(f.read())


def generate_commit_proof(commit_hash: str) -> str:
    private_key = load_private_key()
    instructor_pub = load_instructor_public_key()

    signature = rsa_sign_pss_sha256(private_key, commit_hash.encode("utf-8"))

    encrypted_sig = instructor_pub.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    return base64.b64encode(encrypted_sig).decode("utf-8")
