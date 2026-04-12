from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])

def hash_password(plain_password: str) -> str:
    plain_password = plain_password[:72]
    return password_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool: 
    plain_password = plain_password[:72]
    return password_context.verify(plain_password, hashed_password)