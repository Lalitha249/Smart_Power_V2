from datetime import datetime, timedelta
from models.subscription_model import ( get_plan, create_plan, get_subscription, upsert_subscription, update_subscription)
from models.user_model import find_user_by_id
from services.email_service import send_email,send_subscription_expired,send_subscription_reminder
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

    # -----------------------------
    # Upgrade Rule A
    # Reset duration on upgrade
    # -----------------------------

    start_date = datetime.utcnow()
    duration = plan.get("duration_days", 30)
    end_date = start_date + timedelta(days=duration)

    subscription_data = {
        "user_id": user_id,
        "plan_id": plan_id,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
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

#----------check subscription expiry and send notifications----------
def check_subscription_expiry_and_notify():
    from datetime import datetime, timedelta

    today = datetime.utcnow()
    tomorrow = today + timedelta(days=1)

    # Find all active subscriptions
    subscriptions = db.subscriptions.find({"status": "active"})

    for sub in subscriptions:
        user_id = sub["user_id"]
        end_date = sub["end_date"]

        # Fetch user email
        user = find_user_by_id(user_id)
        if not user:
            continue

        email = user.get("email")

        # 1️⃣ Reminder: 1 day before expiry
        if today.date() == (end_date.date() - timedelta(days=1)):
            send_email(
                to=email,
                subject="Subscription Expiring Tomorrow",
                body="Your subscription will expire tomorrow. Please renew."
            )

        # 2️⃣ Expired
        if today > end_date:
            db.subscriptions.update_one(
                {"user_id": user_id},
                {"$set": {"status": "expired"}}
            )

            send_email(
                to=email,
                subject="Subscription Expired",
                body="Your subscription has expired. Please renew to continue services."
            )

def get_subscription_service(user_id: str):

    subscription = get_subscription(user_id)

    if not subscription:
        return {"error": "Subscription not found"}, 404

    # -----------------------------
    # Expiry Check
    # -----------------------------
    today = datetime.utcnow()

    if today > subscription["end_date"]:
        update_subscription(user_id, {"status": "expired"})
        subscription["status"] = "expired"
    subscription["start_date"] = subscription["start_date"].isoformat()
    subscription["end_date"] = subscription["end_date"].isoformat()

    return {"subscription": subscription}, 200

