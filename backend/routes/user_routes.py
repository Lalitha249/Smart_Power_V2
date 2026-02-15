from flask import Blueprint
from controllers.user_controller import register_user_controller,get_users_controller,register_user_controller,verify_email_controller

user_bp = Blueprint("user_bp", __name__)
user_bp.post("/register")(register_user_controller)
user_bp.get("/users")(get_users_controller)
user_bp.get("/verify-email")(verify_email_controller)
