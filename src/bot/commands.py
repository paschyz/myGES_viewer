import discord
from client import MyClient
from utils import *
from config import *

from scrapper.utils import *


def setup_commands(client: MyClient):
    client_mongo, collection_marks, collection_planning, collection_trombinoscope, collection_users = connect_to_mongo(
        mongo_db_key)

    @client.event
    async def on_ready():
        try:
            connect_to_mongo(mongo_db_key)
            print(
                '-- Connection to MongoDB successful.\n-- Logged in as {0.user}!'.format(client))
        except Exception as e:
            print(f"-- Error connecting to MongoDB: {str(e)}")

    @client.tree.command(description="Voir les commandes disponibles")
    async def help(interaction: discord.Interaction):
        embed = discord.Embed(
            title="Commandes disponibles:", description="", color=discord.Color.blue())

        for command in client.tree.walk_commands():
            if isinstance(command, discord.app_commands.Group):
                subcommands = [
                    f"{command.qualified_name} {subcommand.qualified_name}" for subcommand in command.commands]
                value = ', '.join(subcommands)
            else:
                value = command.description
            embed.add_field(
                name=f"/{command.qualified_name}", value=value, inline=False)

        await interaction.response.send_message(embed=embed)

    # ... existing code ...
    @client.tree.command(description="Voir ses notes")
    async def notes(interaction: discord.Interaction):
        if not await verify_if_user_exists(interaction, collection_marks):
            return
        embeds = []
        try:
            documents_marks = collection_marks.find(
                {"user_discord_id": interaction.user.id})
            await display_marks(interaction, documents_marks)
        except Exception as e:
            print(f"-- Error : {str(e)}")

    @client.tree.command(description="Se connecter à MYges")
    async def login(interaction: discord.Interaction, username: str, password: str):
        await perform_login(interaction, username, password)

    @client.tree.command(description="Permet de mettre à jour ses notes, planning et trombinoscope")
    async def scrape(interaction: discord.Interaction):
        await interaction.response.send_message(f'Starting scrapping...')

        download_dir = os.path.join(os.getcwd(), 'src/scrapper/json')
        await run_scraper(interaction.user,  download_dir)
        await interaction.channel.send(f'Srapping done !')

    @client.tree.command(description="Voir l'emploi du temps")
    async def planning(interaction: discord.Interaction):
        if not await verify_if_user_exists(interaction, collection_planning):
            return
        embeds = []
        try:
            documents_planning = collection_planning.find(
                {"user_discord_id": interaction.user.id})
            await display_planning(interaction, documents_planning)
        except Exception as e:
            print(f"-- Error : {str(e)}")

    @client.tree.command(description="Voir le corps étudiant et enseignant")
    async def trombinoscope(interaction: discord.Interaction):
        if not await verify_if_user_exists(interaction, collection_trombinoscope):
            return
        embeds = []
        try:
            documents_trombinoscope = collection_trombinoscope.find(
                {"user_discord_id": interaction.user.id})
            await display_trombinoscope(interaction, documents_trombinoscope)
        except Exception as e:
            print(f"-- Error : {str(e)}")
