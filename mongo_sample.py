"""MongoDB CRUD sample for Python and MongoDB Compass.

Run this after installing the requirements and starting MongoDB.
"""
from datetime import datetime
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

MONGODB_URI = getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = getenv("MONGODB_DB", "raraphsopvt")

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client[MONGODB_DB]
tasks_collection = db.tasks


def create_task(title: str, description: str) -> str:
    document = {
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    result = tasks_collection.insert_one(document)
    return str(result.inserted_id)


def get_task(task_id: str) -> dict | None:
    try:
        document = tasks_collection.find_one({"_id": ObjectId(task_id)})
    except Exception:
        return None
    return document


def update_task(task_id: str, data: dict) -> bool:
    try:
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": data},
        )
        return result.modified_count > 0
    except Exception:
        return False


def delete_task(task_id: str) -> bool:
    try:
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0
    except Exception:
        return False


def list_tasks() -> list[dict]:
    return list(tasks_collection.find().sort("created_at", -1))


if __name__ == "__main__":
    try:
        print("Connecting to MongoDB at", MONGODB_URI)
        print("Database:", MONGODB_DB)

        task_id = create_task("Learn MongoDB Compass", "Connect Python to MongoDB and inspect collections.")
        print("Created task id:", task_id)

        task = get_task(task_id)
        print("Fetched task:", task)

        updated = update_task(task_id, {"completed": True})
        print("Updated task completed:", updated)

        tasks = list_tasks()
        print("All tasks count:", len(tasks))

        deleted = delete_task(task_id)
        print("Deleted task:", deleted)
    except PyMongoError as exc:
        print("MongoDB error:", exc)
    finally:
        client.close()
