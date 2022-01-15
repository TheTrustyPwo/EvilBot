import nextcord
from typing import List
from nextcord import slash_command, Client, Interaction, SlashOption, Member, InteractionMessage, Embed
from nextcord.ext import commands
from utils import Configuration
from games import Akinator, TicTacToe

GUILD_IDS = [825894722324922438, 928845819392716840]


class Games(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="tictactoe", description="Play tictactoe", guild_ids=GUILD_IDS)
    async def tictactoe(self, interaction: Interaction,
                        user: Member = SlashOption(name="user", description="Challenge someone!", required=True)):
        await interaction.response.send_message(f"**{interaction.user.name} vs {user.name}**\n\nTurn: {interaction.user.mention} (**X**)", view=TicTacToe.TicTacToe(interaction.user, user))

    @slash_command(name="akinator", description="The classic Akinator game!", guild_ids=GUILD_IDS)
    async def akinator(self, interaction: Interaction):
        akinator = Akinator.Aki()
        await akinator.start()
        await interaction.response.send_message(content="a", view=akinator.view(), embed=akinator.embed())


def setup(client: Client):
    client.add_cog(Games(client))
