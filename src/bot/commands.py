import discord
from client import MyClient


def setup_commands(client: MyClient):

    @client.event
    async def on_ready():
        print('Logged in as {0.user}!'.format(client))

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
    async def scrap(interaction: discord.Interaction):
        await interaction.response.send_message(f'Permet de mettre à jour ses notes, planning et trombinoscope')

    @client.tree.command(description="Voir ses notes")
    async def notes(interaction: discord.Interaction):
        await interaction.response.send_message(f'Voir ses notes')

    @client.tree.command(description="Voir l'emploi du temps")
    async def planning(interaction: discord.Interaction):
        await interaction.response.send_message(f'Voir l\'emploi du temps')

    @client.tree.command(description="Voir le corps étudiant et enseignant")
    async def trombinoscope(interaction: discord.Interaction):
        await interaction.response.send_message(f'Voir le corps étudiant et enseignant')
