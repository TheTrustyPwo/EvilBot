from akinator.async_aki import Akinator
import akinator
import asyncio
import nextcord
from nextcord import Interaction
from utils import Embed


class Aki:
    """Akinator Game"""

    def __init__(self, language: str = "en"):
        self.game = None
        self.aki = Akinator()
        self.language = language

    async def start(self):
        self.game = await self.aki.start_game(self.language)

    async def end(self):
        await self.aki.win()

    async def back(self):
        await self.aki.back()

    async def answer(self, answer: str):
        self.game = await self.aki.answer(answer)

    def question(self):
        return self.game

    def score(self):
        return 0 if self.aki.step is None else self.aki.step

    def ended(self) -> bool:
        return self.aki.progression >= 80 or self.aki.step >= 80

    def embed(self):
        return Embed.getEmbed("Akinator", [("%score%", self.score() + 1), ("%question%", self.question())])

    def view(self):
        return self.Buttons(self)

    class Buttons(nextcord.ui.View):
        def __init__(self, aki):
            super().__init__()
            self.value = None
            self.aki = aki

        @nextcord.ui.button(label="Yes", emoji="👍", style=nextcord.ButtonStyle.primary)
        async def yes(self, button: nextcord.ui.Button, interaction: Interaction):
            await self.aki.answer("y")
            message = await interaction.original_message()
            await message.edit(embed=self.aki.embed(), view=self.aki.view())

        @nextcord.ui.button(label="No", emoji="👎", style=nextcord.ButtonStyle.primary)
        async def no(self, button: nextcord.ui.Button, interaction: Interaction):
            await self.aki.answer("n")

        @nextcord.ui.button(label="Don't know", emoji="❔", style=nextcord.ButtonStyle.primary)
        async def dont_know(self, button: nextcord.ui.Button, interaction: Interaction):
            await self.aki.answer("i")

        @nextcord.ui.button(label="Probably", emoji="🤔", style=nextcord.ButtonStyle.primary)
        async def probably(self, button: nextcord.ui.Button, interaction: Interaction):
            await self.aki.answer("p")

        @nextcord.ui.button(label="Probably Not", emoji="🙄", style=nextcord.ButtonStyle.primary)
        async def probably_not(self, button: nextcord.ui.Button, interaction: Interaction):
            await self.aki.answer("pn")
