from db.mongo import db


# -----------------------------------------
# INSERT USAGE LOG
# -----------------------------------------
def insert_usage_log(data: dict):
    return db.usage_logs.insert_one(data)


# -----------------------------------------
# GET ALL USAGE BY USER & MONTH
# -----------------------------------------
def get_user_usage_by_month(user_id: str, month: str):
    return list(
        db.usage_logs.find(
            {"user_id": user_id, "month": month},
            {"_id": 0}
        )
    )


# -----------------------------------------
# GET TOTAL UNITS BY USER & MONTH
# -----------------------------------------
def get_total_usage(user_id: str, month: str):
    pipeline = [
        {
            "$match": {
                "user_id": user_id,
                "month": month
            }
        },
        {
            "$group": {
                "_id": None,
                "total_units": {"$sum": "$units_consumed"}
            }
        }
    ]

    result = list(db.usage_logs.aggregate(pipeline))

    if result:
        return result[0]["total_units"]

    return 0
