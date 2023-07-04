from client import MyClient
from config import myges_viewer_key, intents
from commands import setup_commands

client = MyClient(intents=intents)
setup_commands(client)

client.run(myges_viewer_key)
