from hashlib import sha256
from cryptography.hazmat.primitives import constant_time

def hash_pw(password: str, username: str) -> str:
    hash = sha256(f"{password}{username}".encode()).hexdigest()

    return hash


def verify(hash: str, password: str, email: str) -> bool:

    potential_hash: str = hash_pw(password=password, username=email)

    print(hash, potential_hash)
    if constant_time.bytes_eq(potential_hash.encode(), hash.encode()):
        return True
    return False