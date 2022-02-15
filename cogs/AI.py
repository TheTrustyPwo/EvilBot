import json
import datetime

import nextcord
import openai
from nextcord import slash_command, Client, Interaction, SlashOption, Member, Message, Embed, DMChannel
from nextcord.ext import commands

from utils.Configuration import *

CACHE_FILE = "ai_cache.json"
openai.api_key = get()["OpenAI-Key"]
completion = openai.Completion()


def set_default(user: Member, data: dict):
    if not data.__contains__(str(user.id)):
        data[str(user.id)] = {"Personality": "The AI is friendly, funny and helpful.", "Cache": []}


def set_personality(user: Member, personality: str):
    with open(CACHE_FILE, 'r') as file:
        data = json.load(file)
    set_default(user, data)
    data[str(user.id)]["Personality"] = personality
    with open(CACHE_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def get_personality(user: Member) -> str:
    with open(CACHE_FILE, 'r') as file:
        data = json.load(file)
    set_default(user, data)
    return data[str(user.id)]["Personality"]


def add_cache(user: Member, question: str, answer: str):
    with open(CACHE_FILE, 'r') as file:
        data = json.load(file)
    set_default(user, data)
    cache: list = data[str(user.id)]["Cache"]
    if len(cache) >= 25:
        cache.pop()
    cache.append(f"Human: {question}\nAI: {answer}")
    with open(CACHE_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def get_cache(user: Member) -> list:
    with open(CACHE_FILE, 'r') as file:
        data = json.load(file)
    set_default(user, data)
    return data[str(user.id)]["Cache"]


def clear_cache(user: Member):
    with open(CACHE_FILE, 'r') as file:
        data = json.load(file)
    set_default(user, data)
    data[str(user.id)]["Cache"] = []
    with open(CACHE_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def chat(user: Member, message: str) -> str:
    personality = get_personality(user)
    cache = '\n'.join(get_cache(user))
    prompt = f"The following is a conversation with an AI chatbot. {personality}\n{cache}Human: {message}\nAI:"
    response = completion.create(
        prompt=prompt, engine="curie", stop=['Human', 'human', 'AI'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=100)
    response = response.choices[0].text.strip()
    add_cache(user, message, response)
    return response


class AI(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if (message.channel.id != 931535796564004874) or message.author == self.client.user or message.content.startswith("."):
            return
        async with message.channel.typing():
            response = chat(message.author, message.content)
        await message.reply(response)

    @slash_command(name="ai", description="Commands related to your AI chatbot", guild_ids=get_guild_ids(), force_global=get_global())
    async def ai(self, interaction: Interaction):
        pass

    @ai.subcommand(name="personality", description="View your chatbot's personality")
    async def personality(self, interaction: Interaction):
        personality = get_personality(interaction.user)
        embed = Embed(title=f"{interaction.user.display_name}'s Chatbot Personality", description=personality,
                      color=0xFFA500, timestamp=datetime.datetime.utcnow())
        await interaction.response.send_message(embed=embed)

    @ai.subcommand(name="clearcache",
                   description="Clears all chat cache (Last 25 interactions); Use with caution!")
    async def clear_cache(self, interaction: Interaction):
        clear_cache(interaction.user)
        embed = Embed(title=f"✅ Successfully cleared chatbot cache!",
                      description="Chat with it for it to gain some context on the conversation!",
                      color=0x42ba96, timestamp=datetime.datetime.utcnow())
        await interaction.response.send_message(embed=embed)

    @ai.subcommand(name="set_personality", description="Set your chatbot's personality!")
    async def set_personality(self, interaction: Interaction, personality: str = SlashOption(name="personality",
                                                                                             description="Describe how you want your bot to be!",
                                                                                             required=True)):
        set_personality(interaction.user, personality)
        embed = Embed(title=f"✅ Successfully set chatbot personality", description=f"Personality set to: {personality}",
                      color=0x42ba96, timestamp=datetime.datetime.utcnow())
        await interaction.response.send_message(embed=embed)


def setup(client: Client):
    client.add_cog(AI(client))
