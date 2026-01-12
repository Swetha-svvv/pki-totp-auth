import subprocess
from commit_proof import generate_commit_proof

commit_hash = subprocess.check_output(
    ["git", "log", "-1", "--format=%H"]
).decode().strip()

encrypted_signature = generate_commit_proof(commit_hash)

print("\nCOMMIT HASH:")
print(commit_hash)

print("\nENCRYPTED COMMIT SIGNATURE (SUBMIT THIS):")
print(encrypted_signature)
