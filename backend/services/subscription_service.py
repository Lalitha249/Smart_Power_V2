from datetime import datetime, timedelta
from models.subscription_model import (
    get_plan,
    create_plan,
    get_subscription,
    upsert_subscription,
    update_subscription
)
from models.user_model import find_user_by_id
from services.email_service import send_subscription_expired, send_subscription_reminder
from db.mongo import db


# -----------------------------------------
# PLAN SERVICE METHODS
# -----------------------------------------

def add_plan_service(data: dict):

    plan_id = data.get("plan_id")

    if not plan_id:
        return {"error": "plan_id is required"}, 400

    # prevent duplicate plan_id
    existing = get_plan(plan_id)
    if existing:
        return {"error": "Plan already exists"}, 409

    data["created_at"] = datetime.utcnow()

    create_plan(data)

    return {"message": "Plan created successfully"}, 201


# -----------------------------------------
# SUBSCRIPTION SERVICE METHODS
# -----------------------------------------

def subscribe_user_service(data: dict):

    user_id = data.get("user_id")
    plan_id = data.get("plan_id")

    if not user_id or not plan_id:
        return {"error": "user_id and plan_id are required"}, 400

    # validate user exists
    user = find_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404

    # validate plan exists
    plan = get_plan(plan_id)
    if not plan or not plan.get("is_active", True):
        return {"error": "Plan not available"}, 404

    start_date = datetime.utcnow()
    duration = plan.get("duration_days", 30)
    end_date = start_date + timedelta(days=duration)
    #end_date = start_date + timedelta(minutes=1)

    subscription_data = {
        "user_id": user_id,
        "plan_id": plan_id,
        "start_date": start_date,
        "end_date": end_date,
        "status": "active"
    }

    upsert_subscription(subscription_data)

    return {
        "message": "Subscription activated",
        "subscription": {
            "user_id": user_id,
            "plan_id": plan_id,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "status": "active"
        }
    }, 200


# -----------------------------------------
# SAFE SCHEDULER FUNCTION
# -----------------------------------------

def check_subscription_expiry_and_notify():
    try:
        today = datetime.utcnow()
        subscriptions = db.subscriptions.find({"status": "active"})

        for sub in subscriptions:
            try:
                user_id = sub.get("user_id")
                end_date = sub.get("end_date")

                # Fix string issue safely
                if isinstance(end_date, str):
                    end_date = datetime.fromisoformat(end_date)

                user = find_user_by_id(user_id)
                if not user:
                    continue

                email = user.get("email")
                name = user.get("name", "User")

                # Reminder (1 day before expiry)
                if today.date() == (end_date.date() - timedelta(days=1)):
                    send_subscription_reminder(email, name)

                # Expired
                if today > end_date:
                    db.subscriptions.update_one(
                        {"user_id": user_id},
                        {"$set": {"status": "expired"}}
                    )
                    send_subscription_expired(email, name)

            except Exception as inner_error:
                print("Error processing one subscription:", inner_error)

    except Exception as outer_error:
        print("Scheduler crashed:", outer_error)


# -----------------------------------------
# GET SUBSCRIPTION
# -----------------------------------------

def get_subscription_service(user_id: str):

    subscription = get_subscription(user_id)

    if not subscription:
        return {"error": "Subscription not found"}, 404

    today = datetime.utcnow()

    if today > subscription["end_date"]:
        update_subscription(user_id, {"status": "expired"})
        subscription["status"] = "expired"

    subscription["start_date"] = subscription["start_date"].isoformat()
    subscription["end_date"] = subscription["end_date"].isoformat()

    return {"subscription": subscription}, 200
