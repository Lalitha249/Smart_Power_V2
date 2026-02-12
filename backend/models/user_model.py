from db.mongo import db

def find_user_by_id(user_id):
    return db.users.find_one({"user_id": user_id})

def find_user_by_email(email):
    return db.users.find_one({"email": email})

def insert_user(user_data):
    return db.users.insert_one(user_data)

def get_all_users():
    return list(db.users.find({}, {"_id": 0}))
