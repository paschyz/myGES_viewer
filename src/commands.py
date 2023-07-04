from client import MyClient


def setup_commands(client: MyClient):

    @client.event
    async def on_ready():
        print('Logged in as {0.user}!'.format(client))
