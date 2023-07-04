import discord
from client import MyClient


def setup_commands(client: MyClient):

    @client.event
    async def on_ready():
        print('Logged in as {0.user}!'.format(client))

    @client.tree.command(description="hi")
    async def hi(interaction: discord.Interaction):
        await interaction.response.send_message(f'hello, {interaction.user.name} !')

    @client.tree.command(description="je peux rejoindre votre groupe ouuuuu")
    async def join(interaction: discord.Interaction):
        await interaction.response.send_message(f'Dsl {interaction.user.name}, mais tu n\'es pas sur la liste prioritaire')
