def secure_headers() -> dict:
    return {"X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY"}
