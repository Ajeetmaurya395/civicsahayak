"""MongoDB connection and collections for CivicOS.

Stores ONLY application data — never scheme data (that lives in OpenSearch).
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

_client: Optional[AsyncIOMotorClient] = None
_db = None


async def connect_db():
    """Connect to MongoDB."""
    global _client, _db
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/civicos")
    _client = AsyncIOMotorClient(uri)
    _db = _client.get_default_database()
    print(f"[DB] Connected to MongoDB: {uri}")


async def close_db():
    """Close MongoDB connection."""
    global _client
    if _client:
        _client.close()
        print("[DB] MongoDB connection closed")


def get_db():
    """Get the database instance."""
    return _db


# Collection accessors
def users_collection():
    return _db["users"]

def conversations_collection():
    return _db["conversations"]

def profiles_collection():
    return _db["profiles"]

def saved_schemes_collection():
    return _db["saved_schemes"]

def search_history_collection():
    return _db["search_history"]
