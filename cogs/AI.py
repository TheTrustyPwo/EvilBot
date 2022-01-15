import requests
from nextcord import Client, Message, Webhook, utils
from nextcord.ext import commands

AI_CHANNELS = [931535796564004874]


class AI(commands.Cog):
    """AI Chat"""

    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.client.user or message.author.name == "AI":
            return
        if not AI_CHANNELS.__contains__(message.channel.id):
            return
        async with message.channel.typing():
            response = requests.get(
                url=f"http://api.brainshop.ai/get?bid=158466&key=EHtEv7tH2K3TG9VO&uid={message.author.id}&msg={message.content}")
            reply = response.json()['cnt']
            await message.reply(content=f"`AI:` {reply}")


def setup(client: Client):
    client.add_cog(AI(client))
