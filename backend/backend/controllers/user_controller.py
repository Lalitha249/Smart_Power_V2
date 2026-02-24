from flask import request, jsonify
from services.user_service import register_user_service,get_users_service,verify_email_service


def register_user_controller():
    body = request.get_json(force=True, silent=True) or {}

    response, status = register_user_service(body)

    return jsonify(response), status

def get_users_controller():
    response, status = get_users_service()
    return jsonify(response), status

def verify_email_controller():
    token = request.args.get("token")
    response, status = verify_email_service(token)
    print("VERIFY ROUTE HIT")

    return jsonify(response), status