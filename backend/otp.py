import random
import time

OTP_STORE = {}  # email -> {otp, expiry}

def generate_otp(email: str):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[email] = {
        "otp": otp,
        "expiry": time.time() + 300  # 5 minutes
    }
    return otp

def verify_otp(email: str, user_otp: str) -> bool:
    record = OTP_STORE.get(email)
    if not record:
        return False
    if time.time() > record["expiry"]:
        return False
    return record["otp"] == user_otp
