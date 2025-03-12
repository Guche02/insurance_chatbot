import os
import pymongo

mongo_url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(mongo_url)
db = client.insurance_chat_history
login_collection = db.login_chat_history
enrollment_collection = db.enrollment_chat_history

def get_latest_chat(category, oldest_timestamp):
    if category == "login":
        collection = login_collection
    elif category == "enrollment":
        collection = enrollment_collection
    latest_chat= collection.find_one({"created_at": {"$gt": oldest_timestamp}},  sort=[("created_at", -1)])
    latest_chat_question = latest_chat['question'] if latest_chat else ""
    latest_chat_answer = latest_chat['answer'] if latest_chat else ""
    latest_chat_formatted = f"User: {latest_chat_question} AI: {latest_chat_answer}" if latest_chat else ""
    return latest_chat_formatted


def get_chat_history(category, oldest_timestamp):
    if category == "login":
        collection = login_collection
    elif category == "enrollment":
        collection = enrollment_collection
    return list(collection.find({"created_at": {"$gt": oldest_timestamp}}).sort("created_at", -1).limit(3))

def add_collection(category,data):
    if category == "login":
        collection = login_collection
    elif category == "enrollment":
        collection = enrollment_collection
    collection.insert_one(data)
