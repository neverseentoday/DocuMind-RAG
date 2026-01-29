import sys
import os
import requests
import streamlit as st

# Make backend importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

API_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Chatbot", layout="centered")
st.title("🤖 PDF RAG Chatbot")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "email" not in st.session_state:
    st.session_state.email = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

if "pending_employee_query" not in st.session_state:
    st.session_state.pending_employee_query = None

# ---------------- CHAT DISPLAY ----------------
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.write(msg)

# ---------------- USER INPUT ----------------
user_query = st.chat_input("Ask something about the PDF...")

if user_query:
    # Show user message
    st.session_state.messages.append(("user", user_query))
    with st.chat_message("user"):
        st.write(user_query)

    payload = {"query": user_query}
    if st.session_state.email:
        payload["email"] = st.session_state.email

    response = requests.post(f"{API_URL}/chat", json=payload).json()

    # -------- EMPLOYEE AUTH FLOW --------
    if response.get("action") == "REQUEST_EMAIL":
        st.session_state.pending_employee_query = user_query
        with st.chat_message("assistant"):
            st.write("🔐 This question involves employee data.")
            st.write("Please enter your email to receive an OTP.")

    elif response.get("action") == "SEND_OTP":
        st.session_state.pending_employee_query = user_query
        with st.chat_message("assistant"):
            st.write("📧 OTP verification required.")
            st.write("Enter your email below to receive an OTP.")

    # -------- NORMAL ANSWER (PDF or VERIFIED EMPLOYEE) --------
    elif "answer" in response:
        st.session_state.messages.append(("assistant", response["answer"]))
        with st.chat_message("assistant"):
            st.write(response["answer"])

# ---------------- EMAIL INPUT ----------------
if st.session_state.pending_employee_query and not st.session_state.email:
    email = st.text_input("Enter your email to receive OTP")

    if st.button("Send OTP") and email:
        requests.post(f"{API_URL}/send-otp", params={"email": email})
        st.session_state.email = email
        with st.chat_message("assistant"):
            st.write("✅ OTP has been sent to your email.")

# ---------------- OTP INPUT ----------------
if st.session_state.email and not st.session_state.otp_verified:
    otp = st.text_input("Enter OTP", max_chars=6)

    if st.button("Verify OTP") and otp:
        res = requests.post(
            f"{API_URL}/verify-otp",
            params={"email": st.session_state.email, "otp": otp}
        )

        if res.status_code == 200:
            st.session_state.otp_verified = True
            with st.chat_message("assistant"):
                st.write("✅ OTP verified successfully!")

            # Retry the pending employee query automatically
            payload = {
                "query": st.session_state.pending_employee_query,
                "email": st.session_state.email
            }
            retry_response = requests.post(f"{API_URL}/chat", json=payload).json()

            if "answer" in retry_response:
                st.session_state.messages.append(("assistant", retry_response["answer"]))
                with st.chat_message("assistant"):
                    st.write(retry_response["answer"])

            st.session_state.pending_employee_query = None
        else:
            with st.chat_message("assistant"):
                st.write("❌ Invalid or expired OTP. Try again.")
