# routes/reward_routes.py

from flask import Blueprint
from controllers.reward_controller import (
    get_rewards,
    patch_rewards
)
reward_bp = Blueprint("reward_bp", __name__)

reward_bp.route(
    "/users/<user_id>/rewards",
    methods=["GET"]
)(get_rewards)

reward_bp.route(
    "/users/<user_id>/rewards",
    methods=["PATCH"]
)(patch_rewards)