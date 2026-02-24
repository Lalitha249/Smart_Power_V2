from flask import Blueprint
from controllers.usage_controller import (
    add_usage_controller,
    get_usage_summary_controller
)

usage_bp = Blueprint("usage", __name__, url_prefix="/usage")


# -----------------------------------------
# ADD USAGE
# -----------------------------------------
@usage_bp.route("/add", methods=["POST"])
def add_usage():
    return add_usage_controller()


# -----------------------------------------
# GET USAGE SUMMARY
# -----------------------------------------
@usage_bp.route("/summary/<user_id>", methods=["GET"])
def get_usage_summary(user_id):
    return get_usage_summary_controller(user_id)
