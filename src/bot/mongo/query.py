from pymongo import MongoClient
from dotenv import load_dotenv
import discord

import os

load_dotenv()
myges_viewer_key = os.getenv("DISCORD_BOT_KEY")

mongo_db_key = os.getenv("MONGO_DB_KEY")

guild_id_myges_viewer = os.getenv("GUILD_ID_MYGES_VIEWER")
MY_GUILD = discord.Object(id=guild_id_myges_viewer)

client_mongo = MongoClient(
    mongo_db_key)
db = client_mongo["myGES"]
collection_marks = db["marks"]
collection_planning = db["planning"]
collection_trombinoscope = db["trombinoscope"]
collection_users = db["users"]
filter = {}

# Define the update operation to set the user_discord_id field as an integer
update = {"$set": {"user_discord_id": 314809676447350785}}

# Use the update_many method to update the matching documents
result = collection_planning.update_many(filter, update)
print("Number of documents updated:", result.modified_count)
