from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_pw(pw : str) -> str:
    return password_hash(pw)

def verify_password(pw: str, hashed_pw: str) -> bool:
    return password_hash.verify(pw, hashed_pw)
    