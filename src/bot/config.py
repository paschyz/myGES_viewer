import os
import discord
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
myges_viewer_key = os.getenv("DISCORD_BOT_KEY")

mongo_db_key = os.getenv("MONGO_DB_KEY")

guild_id_myges_viewer = os.getenv("GUILD_ID_MYGES_VIEWER")
MY_GUILD = discord.Object(id=guild_id_myges_viewer)

client_mongo = MongoClient(
    mongo_db_key)
db = client_mongo["myGES"]
users_collection = db["users"]

intents = discord.Intents.default()
