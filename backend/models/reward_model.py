# models/reward_model.py

from db.mongo import db
from datetime import datetime

# Ensure unique index (run once at startup manually if needed)
db.rewards.create_index("user_id", unique=True)


def get_reward(user_id: str):
    return db.rewards.find_one(
        {"user_id": user_id},
        {"_id": 0}
    )


def upsert_reward(user_id: str, points: int):
    return db.rewards.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "user_id": user_id,
                "reward_points": points,
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )


def reset_reward(user_id: str):
    return db.rewards.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "reward_points": 0,
                "updated_at": datetime.utcnow()
            }
        }
    )