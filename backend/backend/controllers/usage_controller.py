from flask import request, jsonify
from services.usage_service import (
    add_usage_service,
    get_usage_summary_service
)


# -----------------------------------------
# ADD USAGE CONTROLLER
# -----------------------------------------
def add_usage_controller():
    data = request.get_json()
    response, status = add_usage_service(data)
    return jsonify(response), status


# -----------------------------------------
# GET USAGE SUMMARY CONTROLLER
# -----------------------------------------
def get_usage_summary_controller(user_id):
    response, status = get_usage_summary_service(user_id)
    return jsonify(response), status
