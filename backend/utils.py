def classify_query(query: str) -> str:
    keywords = ["employee", "email", "phone", "id", "emp"]
    return "EMPLOYEE" if any(k in query.lower() for k in keywords) else "PDF"
