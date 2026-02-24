# services/reward_service.py

from models.reward_model import (
    get_reward,
    upsert_reward,
    reset_reward
)


# -----------------------------------
# CALCULATION LOGIC
# -----------------------------------

def calculate_rewards(month_used: float, plan_limit: float) -> int:

    if plan_limit == 0:
        return 0

    usage_percent = (month_used / plan_limit) * 100

    if usage_percent <= 50:
        return 100
    elif usage_percent <= 75:
        return 70
    elif usage_percent <= 90:
        return 40
    elif usage_percent <= 100:
        return 10
    else:
        return 0


# -----------------------------------
# UPDATE REWARD
# -----------------------------------

def update_user_rewards(user_id: str, month_used: float, plan_limit: float):

    points = calculate_rewards(month_used, plan_limit)

    upsert_reward(user_id, points)

    return points


# -----------------------------------
# GET REWARD
# -----------------------------------

def get_user_rewards(user_id: str):

    reward = get_reward(user_id)

    if not reward:
        return 0

    return reward.get("reward_points", 0)


# -----------------------------------
# CLAIM REWARD
# -----------------------------------

def claim_user_rewards(user_id: str):

    reward = get_reward(user_id)

    if not reward:
        return 0

    current_points = reward.get("reward_points", 0)

    if current_points > 0:
        reset_reward(user_id)

    return current_points