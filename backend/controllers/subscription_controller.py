
from flask import request, jsonify
from services.subscription_service import (
    add_plan_service,
    subscribe_user_service,
    get_subscription_service
)
# -----------------------------
# ADD PLAN
# -----------------------------

def add_plan_controller():
    data = request.get_json() or {}
    response, status = add_plan_service(data)
    return jsonify(response), status
# -----------------------------
# SUBSCRIBE USER
# -----------------------------
def subscribe_user_controller():
    data = request.get_json() or {}
    response, status = subscribe_user_service(data)
    return jsonify(response), status
# -----------------------------
# GET SUBSCRIPTION
# -----------------------------
def get_subscription_controller(user_id):
    response, status = get_subscription_service(user_id)
    return jsonify(response), status
