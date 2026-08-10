import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "wifi_security")
MONGO_COLLECTION = os.getenv(
    "MONGO_COLLECTION",
    "security_events"
)


if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not configured")


client = MongoClient(MONGO_URI)

db = client[MONGO_DB]

security_events = db[MONGO_COLLECTION]


def test_connection():
    client.admin.command("ping")
    print("MongoDB connected successfully")


def ensure_collection():
    """
    Create the security_events collection if it doesn't exist.
    """

    if MONGO_COLLECTION not in db.list_collection_names():

        db.create_collection(MONGO_COLLECTION)

        print(
            f"Collection '{MONGO_COLLECTION}' created successfully"
        )

    else:

        print(
            f"Collection '{MONGO_COLLECTION}' already exists"
        )