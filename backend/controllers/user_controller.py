from flask import request, jsonify
from services.user_service import register_user_service,get_users_service


def register_user_controller():
    body = request.get_json(force=True, silent=True) or {}

    response, status = register_user_service(body)

    return jsonify(response), status

def get_users_controller():
    response, status = get_users_service()
    return jsonify(response), status