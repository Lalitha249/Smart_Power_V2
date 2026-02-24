from datetime import datetime
from models.usage_model import (
    insert_usage_log,
    get_total_usage
)
from models.subscription_model import get_subscription, get_plan
from models.user_model import find_user_by_id


# -------------------------------------------------
# ADD USAGE
# -------------------------------------------------
def add_usage_service(data: dict):

    user_id = data.get("user_id")
    device_name = data.get("device_name")
    units = data.get("units_consumed")

    # ---------------- VALIDATION ----------------
    if not user_id or not device_name or units is None:
        return {"error": "user_id, device_name and units_consumed are required"}, 400

    # ---------------- CHECK USER ----------------
    user = find_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404

    # ---------------- CHECK SUBSCRIPTION ----------------
    subscription = get_subscription(user_id)
    if not subscription:
        return {"error": "Subscription not found"}, 404

    if subscription.get("status") != "active":
        return {"error": "Subscription is not active"}, 403

    # ---------------- GET PLAN ----------------
    plan = get_plan(subscription.get("plan_id"))
    if not plan:
        return {"error": "Plan not found"}, 404

    included_units = plan.get("included_units", 0)
    extra_unit_cost = plan.get("extra_unit_cost", 0)

    # ---------------- CURRENT MONTH ----------------
    now = datetime.utcnow()
    month = now.strftime("%Y-%m")

    # ---------------- GET CURRENT TOTAL ----------------
    current_total = get_total_usage(user_id, month)

    new_total = current_total + units

    # ---------------- COST CALCULATION (INCREMENTAL) ----------------

    remaining_free_units = max(included_units - current_total, 0)

    extra_units = 0
    extra_cost = 0
    warning = None

# If this entry crosses the limit
    if units > remaining_free_units:
      extra_units = units - remaining_free_units
      extra_cost = extra_units * extra_unit_cost
      warning = "Usage limit exceeded"


    # ---------------- PREPARE USAGE LOG ----------------
    usage_data = {
        "user_id": user_id,
        "device_name": device_name,
        "units_consumed": units,
        "timestamp": now,
        "month": month,
        "calculated_cost": extra_cost
    }

    insert_usage_log(usage_data)

    return {
        "message": "Usage recorded successfully",
        "data": {
            "current_total_units": new_total,
            "included_units": included_units,
            "extra_units": extra_units,
            "extra_cost": extra_cost,
            "warning": warning
        }
    }, 200
# -------------------------------------------------
# GET USAGE SUMMARY
# -------------------------------------------------
def get_usage_summary_service(user_id: str):

    user = find_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404

    subscription = get_subscription(user_id)
    if not subscription:
        return {"error": "Subscription not found"}, 404

    plan = get_plan(subscription.get("plan_id"))
    if not plan:
        return {"error": "Plan not found"}, 404

    included_units = plan.get("included_units", 0)
    extra_unit_cost = plan.get("extra_unit_cost", 0)

    now = datetime.utcnow()
    month = now.strftime("%Y-%m")

    total_units = get_total_usage(user_id, month)

    extra_units = 0
    total_extra_cost = 0

    if total_units > included_units:
        extra_units = total_units - included_units
        total_extra_cost = extra_units * extra_unit_cost

    return {
        "total_units": total_units,
        "included_units": included_units,
        "extra_units": extra_units,
        "total_extra_cost": total_extra_cost
    }, 200
