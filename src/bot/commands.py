import discord
from client import MyClient
from utils import *
from config import *

def setup_commands(client: MyClient):
    client_mongo, collection_marks, collection_planning, collection_trombinoscope, collection_users = connect_to_mongo(mongo_db_key)

    @client.event
    async def on_ready():
        try:
            connect_to_mongo(mongo_db_key)
            print('-- Connection to MongoDB successful.\n-- Logged in as {0.user}!'.format(client))
        except Exception as e:
            print(f"-- Error connecting to MongoDB: {str(e)}")
            
    @client.tree.command(description="Voir ses notes")
    async def notes(interaction: discord.Interaction):
        if not await verify_if_user_exists(interaction,collection_planning):
            return
        embeds=[]
        try:
            documents_marks = collection_marks.find({"user_discord_id": interaction.user.id})
            await display_marks(interaction,documents_marks)
        except Exception as e:
            print(f"-- Error : {str(e)}")

    @client.tree.command(description="hi")
    async def hi(interaction: discord.Interaction):
        await interaction.response.send_message(f'hello, {interaction.user.name} !')

    @client.tree.command(description="Je peux rejoindre votre groupe ouuuuu")
    async def join(interaction: discord.Interaction):
        await interaction.response.send_message(f'Dsl {interaction.user.name}, mais tu n\'es pas sur la liste prioritaire')

    @client.tree.command(description="Se connecter à MYges")
    async def login(interaction: discord.Interaction):
        await interaction.response.send_message(f'Se connecter à MYges')

    @client.tree.command(description="Permet de mettre à jour ses notes, planning et trombinoscope")
    async def scrape(interaction: discord.Interaction):
        await interaction.response.send_message(f'Permet de mettre à jour ses notes, planning et trombinoscope')

   

    @client.tree.command(description="Voir l'emploi du temps")
    async def planning(interaction: discord.Interaction):
        await interaction.response.send_message(f'Voir l\'emploi du temps')

    @client.tree.command(description="Voir le corps étudiant et enseignant")
    async def trombinoscope(interaction: discord.Interaction):
        await interaction.response.send_message(f'Voir le corps étudiant et enseignant')
    
