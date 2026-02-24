# controllers/reward_controller.py

from flask import request, jsonify
from services.reward_service import (
    get_user_rewards,
    claim_user_rewards
)


def get_rewards(user_id: str):

    points = get_user_rewards(user_id)

    return jsonify({
        "user_id": user_id,
        "reward_points": points
    }), 200


def patch_rewards(user_id: str):

    data = request.get_json()

    if not data or data.get("action") != "claim":
        return jsonify({"error": "Invalid action"}), 400

    claimed_points = claim_user_rewards(user_id)

    return jsonify({
        "user_id": user_id,
        "claimed_points": claimed_points
    }), 200