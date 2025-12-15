import random
from passlib.context import CryptContext

def generate_otp() -> str:
    return f"{random.randint(1000, 9999)}"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
