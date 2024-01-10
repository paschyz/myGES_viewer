import os
import discord
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()
myges_viewer_key = os.getenv("DISCORD_BOT_KEY")

mongo_db_key = os.getenv("MONGO_DB_KEY")

guild_id_myges_viewer = os.getenv("GUILD_ID_MYGES_VIEWER")
guild_id_test = os.getenv("GUILD_ID_TEST")
MY_GUILD = discord.Object(id=guild_id_myges_viewer)

client_mongo = MongoClient(
    mongo_db_key)
db = client_mongo["myGES"]
collection_marks = db["marks"]
collection_planning = db["planning"]
collection_trombinoscope = db["trombinoscope"]
collection_users = db["users"]

login_url = os.getenv("LOGIN_URL")
login_username = os.getenv("LOGIN_USERNAME")
login_password = os.getenv("LOGIN_PASSWORD")

intents = discord.Intents.default()
