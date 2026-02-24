# models/subscription_model.py
from db.mongo import db
from datetime import datetime
# -----------------------------
# PLAN METHODS
# -----------------------------
def get_plan(plan_id: str):
    return db.plans.find_one(
        {"plan_id": plan_id},
        {"_id": 0}
    )
def create_plan(data: dict):
    return db.plans.insert_one(data)
# -----------------------------
# SUBSCRIPTION METHODS
# -----------------------------
def get_subscription(user_id: str):
    return db.subscriptions.find_one(
        {"user_id": user_id},
        {"_id": 0}
    )
def upsert_subscription(data: dict):
    return db.subscriptions.update_one(
        {"user_id": data["user_id"]},
        {"$set": data},
        upsert=True
    )
def update_subscription(user_id: str, fields: dict):
    return db.subscriptions.update_one(
        {"user_id": user_id},
        {"$set": fields}
    )
