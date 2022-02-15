import datetime
import random

from nextcord import slash_command, Client, Interaction, SlashOption
from nextcord.ext import commands

from utils import Embed, Messages
from utils.Configuration import get_guild_ids, get_global


class Utility(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="choose", description="Make the bot choose a random thing", guild_ids=get_guild_ids(),
                   force_global=get_global())
    async def choose(self, interaction: Interaction, *,
                     choices: str = SlashOption(name="choices", description="Separate each choice with ' | '",
                                                required=True)):
        choices = choices.split(" | ")
        if len(choices) < 2:
            await interaction.response.send_message(Messages.getMessage("Choose-Not-Enough-Options"))
            return
        chosen = random.choice(choices)
        await interaction.response.send_message(
            embed=Embed.getEmbed("Choose", [("%chosen%", chosen), ("%number%", len(choices))]))

    @slash_command(name="year", description="Time until the next year!", guild_ids=get_guild_ids(),
                   force_global=get_global())
    async def year(self, interaction: Interaction):
        time = datetime.datetime(datetime.datetime.now().year + 1, 1, 1, 0, 0, 0) - datetime.datetime.now()
        days, hours, minutes, seconds = time.days, time.seconds // 3600, (time.seconds // 60) % 60, (time.seconds % 60)
        await interaction.response.send_message(embed=Embed.getEmbed("Year", [("%days%", days), ("%hours%", hours),
                                                                              ("%minutes%", minutes),
                                                                              ("%seconds%", seconds), ("%next-year%",
                                                                                                       datetime.datetime.now().year + 1)]))


def setup(client: Client):
    client.add_cog(Utility(client))
