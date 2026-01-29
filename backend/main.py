from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

from backend.employees import get_employee
from backend.utils import classify_query
from backend.rag import rag_answer
from backend.otp import generate_otp, verify_otp
from backend.email_utils import send_otp_email

app = FastAPI()

# ---------------- IN-MEMORY STORE ----------------
# Stores emails that have successfully verified OTP
verified_emails = set()

# ---------------- MODELS ----------------
class Chat(BaseModel):
    query: str
    email: str | None = None   # required only for employee queries

# ---------------- OTP ENDPOINTS ----------------
@app.post("/send-otp")
def send_otp(email: str):
    otp = generate_otp(email)
    send_otp_email(email, otp)
    return {"message": "OTP sent to email"}

@app.post("/verify-otp")
def verify(email: str, otp: str):
    if verify_otp(email, otp):
        verified_emails.add(email)
        return {"verified": True}
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

# ---------------- CHAT ENDPOINT ----------------
@app.post("/chat")
def chat(data: Chat):
    intent = classify_query(data.query)

    # ---------- EMPLOYEE QUERIES (OTP PROTECTED) ----------
    if intent == "EMPLOYEE":

        # Step 1: Email required
        if not data.email:
            return {
                "error": "Email required for employee queries",
                "action": "REQUEST_EMAIL"
            }

        # Step 2: OTP verification required
        if data.email not in verified_emails:
            return {
                "error": "OTP verification required",
                "action": "SEND_OTP"
            }

        # Step 3: Process employee query
        match = re.search(r'EMP\d+', data.query)
        if not match:
            return {"answer": "Provide a valid Employee ID"}

        emp = get_employee(match.group())
        if not emp:
            return {"answer": "Employee not found"}

        return {
            "answer": f"""
Name: {emp['name']}
Email: {emp['email']}
Phone: {emp['phone']}
"""
        }

    # ---------- PDF QUERIES (PUBLIC, RAG) ----------
    return {"answer": rag_answer(data.query)}
