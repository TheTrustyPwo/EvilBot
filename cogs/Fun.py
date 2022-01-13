import random
import asyncio
from nextcord import slash_command, Client, Interaction, SlashOption, Member, InteractionMessage, Embed
from nextcord.ext import commands
from utils import Configuration

GUILD_IDS = [825894722324922438]


class Fun(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="say", description="Make the bot say whatever you want", guild_ids=GUILD_IDS)
    async def say(self, interaction: Interaction,
                  text: str = SlashOption(name="text", description="Text to say", required=True)):
        await interaction.response.send_message(text)

    @slash_command(name="spoiler", description="Say a text in annoying spoiler form!", guild_ids=GUILD_IDS)
    async def spoiler(self, interaction: Interaction,
                      text: str = SlashOption(name="text", description="Text to spoil", required=True)):
        string: str = ""
        for char in text:
            string += f"||{char}||"
        await interaction.response.send_message(string)

    @slash_command(name="rickroll", description="Rickroll someone!", guild_ids=GUILD_IDS)
    async def rickroll(self, interaction: Interaction,
                       user: Member = SlashOption(name="user", description="User to rickroll", required=False)):
        if user is None:
            user = random.choice(ctx.guild.members)
        name = f"**{user.name}**"
        full = ""
        emojis = ["🎸", "🎵", "🎼", "🎶", "🎧", "🎻", "🎹", "🎤", "📯", "🎷", "🎺"]
        await interaction.response.send_message(f"RickRolling {user}")
        message: InteractionMessage = await interaction.original_message()
        for line in Configuration.getConfig()["Fun"]["Rickroll"]:
            front = random.choice(emojis)
            back = random.choice(emojis)
            text = line.replace("{user}", name)
            text = text.replace("{}", name)
            final = front + " " + text + " " + back
            await message.edit(content=final)
            full += final
            full += "\n"
            await asyncio.sleep(1)
        await message.edit(nextcord.Embed(title=f"{user} just got rickrolled!", description=full))


def setup(client: Client):
    client.add_cog(Fun(client))
