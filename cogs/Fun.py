import asyncio
import random

import aiohttp
from nextcord import slash_command, Client, Interaction, SlashOption, Member, InteractionMessage
from nextcord.ext import commands

from utils import Configuration, Embed

GUILD_IDS = [825894722324922438, 928845819392716840]
EMOJIS = [
    '( ͡° ͜ʖ ͡°)', '¯\\_(ツ)_/¯', 'ʕ•ᴥ•ʔ', '(▀̿Ĺ̯▀̿ ̿)', '(ง ͠° ͟ل͜ ͡°)ง', 'ಠ_ಠ',
    "̿'̿'\\̵͇̿̿\\з=( ͠° ͟ʖ ͡°)=ε/̵͇̿̿/'̿̿ ̿ ̿ ̿ ̿ ̿", '[̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]', "﴾͡๏̯͡๏﴿ O'RLY?",
    '[̲̅$̲̅(̲̅ ͡° ͜ʖ ͡°̲̅)̲̅$̲̅]', '(ᵔᴥᵔ)', '(¬‿¬)', '(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)', '(づ￣ ³￣)づ', 'ლ(ಠ益ಠლ)', 'ಠ╭╮ಠ', '♪~ ᕕ(ᐛ)ᕗ',
    'ヾ(⌐■_■)ノ♪', '◉_◉', '\\ (•◡•) /', '༼ʘ̚ل͜ʘ̚༽', '┬┴┬┴┤(･_├┬┴┬┴', 'ᕦ(ò_óˇ)ᕤ', '┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻', '（╯°□°）╯︵( .o.)',
    'ಠ‿↼', '◔ ⌣ ◔', '(ノಠ益ಠ)ノ彡┻━┻', '(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)', "̿ ̿ ̿'̿'\̵͇̿̿\з=(•_•)=ε/̵͇̿̿/'̿'̿ ̿", '(;´༎ຶД༎ຶ`)', '♥‿♥',
    'ᕦ(ò_óˇ)ᕤ', '(•_•) ( •_•)>⌐■-■ (⌐■_■)', '⌐╦╦═─ ಠ_ಠ , (¬‿¬)', '˙ ͜ʟ˙', ":')", '(°ロ°)☝', 'ಠ⌣ಠ', '(；一_一)', '( ⚆ _ ⚆ )',
    '☜(⌒▽⌒)☞', "(ʘᗩʘ')", '¯\\(°_o)/¯', 'ლ,ᔑ•ﺪ͟͠•ᔐ.ლ', '(ʘ‿ʘ)', 'ಠ~ಠ', 'ಠ_ಥ', 'ಠ‿↼', '(>ლ)', '(ღ˘⌣˘ღ)', 'ಠoಠ', 'ರ_ರ',
    '◔ ⌣ ◔', '(✿´‿`)', 'ب_ب', '┬─┬﻿ ︵ /(.□. ）', '☼.☼', '^̮^', '(>人<)', '>_>', '(/) (°,,°) (/)', '(･.◤)', '=U',
    '~(˘▾˘~)', '| (• ◡•)| (❍ᴥ❍ʋ)'
]
PARROTS = [
    "<a:tripletsparrot:772747643159838720>",
    "<a:skiparrot:772747641804816385>",
    "<a:shufflefurtherparrot:772747641766281246>",
    "<a:shipitparrot:772747642702528542>",
    "<a:ryangoslingparrot:772747642311802901>",
    "<a:rotatingparrot:772747642597933066>",
    "<a:revertitparrot:772747641854623775>",
    "<a:portalparrot:772747642643415040>",
    "<a:pizzaparrot:772747642551664660>",
    "<a:pearparrots:772747640550195221>",
    "<a:parrot~1:772747640899239936>",
    "<a:papalparrot:772747640940134410>",
    "<a:oldtimeyparrot:772747640848777246>",
    "<a:matrixparrot:772747640604590091>",
    "<a:margaritaparrot:772747641926320149>",
    "<a:luckyparrot:772747643125891122>",
    "<a:loveparrot:772747642480230402>",
    "<a:icecreamparrot:772747641078546453>",
    "<a:harrypotterparrot:772747641440043038>",
    "<a:hamburgerparrot:772747642366197811>",
    "<a:halalparrot:772747640231952394>",
    "<a:fixparrot:772747642320322582>",
    "<a:fiestaparrot:772747642412335136>",
    "<a:fidgetparrot:772747640932794368>",
    "<a:exceptionallyfastparrot:772747640051728404>",
    "<a:dreidelparrot:772747635101925389>",
    "<a:docparrot:772747640432754719>",
    "<a:databaseparrot:772747635471286312>",
    "<a:darkbeerparrot:772747634254413845>",
    "<a:dailyparrot:772747634518654987>",
    "<a:dabparrot:772747634242224128>",
    "<a:cryptoparrot:772747634175246336>",
    "<a:coffeeparrot:772747633755815937>",
    "<a:chillparrot:772747634036834344>",
    "<a:chefparrot:772747633763811339>",
    "<a:braveheartparrot:772747633642438689>",
    "<a:bobrossparrot:772747633512284171>",
    "<a:bluescluesparrot:772747633604558878>",
    "<a:blondesassyparrot:772747633444782090>",
    "<a:bananaparrot:772747632866361345>",
    "<a:asyncparrot:772747633688182834>"
]
WAVE_PARROTS = [
    "<a:wave1parrot:772747642236043274>",
    "<a:wave2parrot:772747642098155520>",
    "<a:wave3parrot:772747641796689931>",
    "<a:wave4parrot:772747642153074718>",
    "<a:wave5parrot:772747641884114955>",
    "<a:wave6parrot:772747642152812574>",
    "<a:wave7parrot:772747642525712445>",
    "<a:wave8parrot:772747642127253505>",
    "<a:wave9parrot:772747642551664640>"
]

test = [
    "hi1",
    "hi2",
    "hi3"
]

class Fun(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="say", description="Make the bot say whatever you want", guild_ids=GUILD_IDS)
    async def say(self, interaction: Interaction,
                  text: str = SlashOption(name="text", description="Text to say", required=True)):
        await interaction.response.send_message(text)

    @slash_command(name="test", description="testing", guild_ids=GUILD_IDS)
    async def test(self, interaction: Interaction):
        await interaction.response.send_message("".join(test))

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
        user = random.choice(interaction.guild.members) if user is None else user
        full = ""
        emojis = ["🎸", "🎵", "🎼", "🎶", "🎧", "🎻", "🎹", "🎤", "📯", "🎷", "🎺"]
        await interaction.response.send_message(f"RickRolling {user}")
        message: InteractionMessage = await interaction.original_message()
        for line in Configuration.getConfig()["Fun"]["Rickroll"]:
            text = line.replace("{user}", f"**{user.name}**").replace("{}", f"**{user.name}**")
            text = random.choice(emojis) + " " + text + " " + random.choice(emojis)
            await message.edit(content=text)
            full = full + text + "\n"
            await asyncio.sleep(1)
        await message.edit(nextcord.Embed(title=f"{user} just got rickrolled!", description=full))

    @slash_command(name="emoji", description="Make the bot say a random emoji", guild_ids=GUILD_IDS)
    async def emoji(self, interaction: Interaction):
        emoji = random.choice(EMOJIS)
        await interaction.response.send_message(emoji)

    @slash_command(name="parrot", description="Replies with a random parrot", guild_ids=GUILD_IDS)
    async def parrot(self, interaction: Interaction):
        parrot = random.choice(PARROTS)
        await interaction.response.send_message(parrot)

    @slash_command(name="parrot_wave", description="Make a wave of parrots!", guild_ids=GUILD_IDS)
    async def parrot_wave(self, interaction: Interaction):
        await interaction.response.send_message(''.join(WAVE_PARROTS))

    @slash_command(name="joke", description="Wanna hear a joke?", guild_ids=GUILD_IDS)
    async def joke(self, interaction: Interaction,
                   category: str = SlashOption(name="category", description="Specify a category",
                                               choices=["Pun", "Programming", "Miscellaneous", "Dark", "Spooky",
                                                        "Christmas"])):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://sv443.net/jokeapi/v2/joke/{category}?safe-mode") as request:
                response = await request.json()
        if response["type"] == "single":
            await interaction.response.send_message(
                embed=Embed.getEmbed("Joke", [("%category%", category), ("%joke%", response["joke"])]))
        elif response["type"] == "twopart":
            await interaction.response.send_message(embed=Embed.getEmbed("Joke", [("%category%", category), (
            "%joke%", f"{response['setup']} \nAnswer: ||{response['delivery']}||")]))


def setup(client: Client):
    client.add_cog(Fun(client))
