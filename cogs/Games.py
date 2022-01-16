import nextcord
from typing import List
from nextcord import slash_command, Client, Interaction, SlashOption, Member, InteractionMessage, Embed
from nextcord.ext import commands
from utils.Configuration import get, get_global, get_guild_ids
from games import Akinator, TicTacToe


class Games(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="tictactoe", description="Play tictactoe", guild_ids=get_guild_ids(), force_global=get_global())
    async def tictactoe(self, interaction: Interaction,
                        user: Member = SlashOption(name="user", description="Challenge someone!", required=True)):
        await interaction.response.send_message(f"**{interaction.user.name} vs {user.name}**\n\nTurn: {interaction.user.mention} (**X**)", view=TicTacToe.TicTacToe(interaction.user, user))

    @slash_command(name="akinator", description="The classic Akinator game!", guild_ids=get_guild_ids(), force_global=get_global())
    async def akinator(self, interaction: Interaction):
        akinator = Akinator.Aki()
        await akinator.start()
        await interaction.response.send_message(content="a", view=akinator.view(), embed=akinator.embed())


def setup(client: Client):
    client.add_cog(Games(client))
