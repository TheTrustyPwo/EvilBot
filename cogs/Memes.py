from collections import deque

import aiohttp
from nextcord import slash_command, Client, Interaction
from nextcord.ext import commands

from utils import Embed

GUILD_IDS = [825894722324922438]
memeHistory = deque()


async def getRedditPosts(subReddit: str, titleFilter=None):
    titleFilter = [] if titleFilter is None else titleFilter
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.reddit.com/r/{subReddit}/hot.json?limit=100") as response:
            request = await response.json()
    for index, val in enumerate(request["data"]["children"]):
        if "title" in val["data"]:
            data = val["data"]
            if not titleFilter.__contains__(data["title"]):
                if data["title"] not in memeHistory:
                    memeHistory.append(data["title"])
                    if len(memeHistory) > 99:
                        memeHistory.popleft()
                        break
                    return data


class Memes(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="showerthoughts", description="Things to think about in the shower", guild_ids=GUILD_IDS)
    async def showerthoughts(self, interaction: Interaction):
        post = await getRedditPosts("showerthoughts")
        await interaction.response.send_message(embed=Embed.getEmbed("ShowerThoughts", [("%title%", post["title"]),
                                                                                        ("%url%", post["url"]),
                                                                                        ("%ups%", post["ups"]), (
                                                                                        "%comments%",
                                                                                        post["num_comments"])]))


def setup(client: Client):
    client.add_cog(Memes(client))
