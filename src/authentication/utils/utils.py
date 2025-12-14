import random

def generate_otp() -> str:
    return f"{random.randint(1000, 9999)}"
