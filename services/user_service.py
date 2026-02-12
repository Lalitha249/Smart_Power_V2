from datetime import datetime, timedelta
import email
from uuid import uuid4
from models.user_model import find_user_by_id, find_user_by_email, insert_user
from services.email_service import send_verification_email


def register_user_service(data):

    user_id = data.get("user_id")
    email = data.get("email")
    name = data.get("name") or (email.split("@")[0] if email else None)

    # ---------------- VALIDATION ----------------
    if not user_id or not email:
        return {"error": "user_id and email are required"}, 400

    # ---------------- CHECK EXISTING USER ----------------
    if find_user_by_id(user_id):
        return {"error": "User already exists"}, 409
    
    # ---------------- CHECK EXISTING EMAIL ----------------
    if find_user_by_email(email):
        return {"error": "Email already registered"}, 409

    # ---------------- CREATE TOKEN ----------------
    verification_token = str(uuid4())
    token_expiry = datetime.utcnow() + timedelta(hours=24)

    # ---------------- PREPARE USER DATA ----------------
    user_data = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "auth_provider": data.get("auth_provider", "local"),
        "email_verified": False,
        "verification_token": verification_token,
        "token_expiry": token_expiry,
        "created_at": datetime.utcnow()
    }

    # ---------------- SAVE TO DB ----------------
    insert_user(user_data)

    # ---------------- SEND EMAIL ----------------
    send_verification_email(email, name, verification_token)

    return {
        "message": "Registration successful. Please verify your email."
    }, 201
