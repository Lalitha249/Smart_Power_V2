# routes/subscription_routes.py

from flask import Blueprint
from controllers.subscription_controller import (
    add_plan_controller,
    subscribe_user_controller,
    get_subscription_controller
)
subscription_bp = Blueprint("subscription_bp", __name__)
# -----------------------------
# ADD PLAN
# -----------------------------
@subscription_bp.route("/plans/add", methods=["POST"])
def add_plan():
    return add_plan_controller()
# -----------------------------
# SUBSCRIBE USER
# -----------------------------
@subscription_bp.route("/plan/subscribe", methods=["POST"])
def subscribe_user():
    return subscribe_user_controller()
# -----------------------------
# GET SUBSCRIPTION
# -----------------------------
@subscription_bp.route("/subscription/<user_id>", methods=["GET"])
def get_subscription(user_id):
    return get_subscription_controller(user_id)
