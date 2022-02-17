import nextcord
from nextcord import slash_command, Client, Interaction, SlashOption, Member, Message
from nextcord.ext import commands

from utils import Database, Embed, Messages, ProvablyFair, NumberUtils
from utils.Configuration import get_global, get_guild_ids

emojis = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]


class HighLow(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    class HighLowView(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None
            self.action = None

        @nextcord.ui.button(label="HI", emoji="⬆", style=nextcord.ButtonStyle.primary)
        async def hi(self, button: nextcord.ui.Button, interaction: Interaction):
            self.value = "HI"
            self.stop()

        @nextcord.ui.button(label="LO", emoji="⬇", style=nextcord.ButtonStyle.primary)
        async def lo(self, button: nextcord.ui.Button, interaction: Interaction):
            self.value = "LO"
            self.stop()

        @nextcord.ui.button(label="Edit Bet", style=nextcord.ButtonStyle.primary, row=1)
        async def edit_bet(self, button: nextcord.ui.Button, interaction: Interaction):
            self.action = "EditBet"
            self.stop()

        @nextcord.ui.button(label="Set Odds", style=nextcord.ButtonStyle.primary, row=1)
        async def set_odds(self, button: nextcord.ui.Button, interaction: Interaction):
            self.action = "SetOdds"
            await interaction.response.send_message("Enter your bet odds (>=1.01, <=4750): ", ephemeral=True)
            self.stop()

        @nextcord.ui.button(label="Set Win Chance", style=nextcord.ButtonStyle.primary, row=1)
        async def set_win_chance(self, button: nextcord.ui.Button, interaction: Interaction):
            self.action = "SetWinChance"
            await interaction.response.send_message("Enter your win chance in percent/% (>=0.02, <=94.06): ",
                                                    ephemeral=True)
            self.stop()

        @nextcord.ui.button(label="Set Client Seed", style=nextcord.ButtonStyle.primary, row=1)
        async def set_client_seed(self, button: nextcord.ui.Button, interaction: Interaction):
            self.action = "SetClientSeed"
            await interaction.response.send_message("Enter your client seed: ",
                                                    ephemeral=True)
            self.stop()

        @nextcord.ui.button(label="❓ How it works?", style=nextcord.ButtonStyle.green, row=2)
        async def how_it_works(self, button: nextcord.ui.button, interaction: Interaction):
            await interaction.response.send_message(Messages.getMessage("HighLow-HowItWorks"), ephemeral=True)

    class EditBet(nextcord.ui.View):
        def __init__(self, client: Client, bet: int, max: int):
            super().__init__()
            self.client = client
            self.bet = bet
            self.max = max
            self.back = False

        def check(self, user: Member):
            def inner_check(message: Message):
                print(message)
                if message.author != user: return False
                try:
                    int(message.content)
                    return True
                except ValueError:
                    return False

            return inner_check

        @nextcord.ui.button(label="/2", style=nextcord.ButtonStyle.primary)
        async def halve(self, button: nextcord.ui.Button, interaction: Interaction):
            self.bet = max(self.bet / 2, 10)
            self.stop()

        @nextcord.ui.button(label="2x", style=nextcord.ButtonStyle.primary)
        async def double(self, button: nextcord.ui.Button, interaction: Interaction):
            self.bet = min(self.bet * 2, self.max)
            self.stop()

        @nextcord.ui.button(label="Min", style=nextcord.ButtonStyle.primary)
        async def min(self, button: nextcord.ui.Button, interaction: Interaction):
            self.bet = 10
            self.stop()

        @nextcord.ui.button(label="Max", style=nextcord.ButtonStyle.primary)
        async def max(self, button: nextcord.ui.Button, interaction: Interaction):
            self.bet = self.max
            self.stop()

        @nextcord.ui.button(label="Custom", style=nextcord.ButtonStyle.primary)
        async def custom(self, button: nextcord.ui.Button, interaction: Interaction):
            message = await self.client.wait_for("message", check=self.check(interaction.user), timeout=30)
            self.bet = int(message.content)
            self.stop()

        @nextcord.ui.button(label="Back", style=nextcord.ButtonStyle.danger)
        async def back(self, button: nextcord.ui.Button, interaction: Interaction):
            self.back = True
            self.stop()

    @slash_command(name="highlow", description="Bet on the high-low game!", guild_ids=get_guild_ids(),
                   force_global=get_global())
    async def highlow(self, interaction: Interaction,
                      bet: int = SlashOption(name="bet", description="How much you want to bet", required=True),
                      client_seed: str = SlashOption(name="client_seed", description="Specify your client seed",
                                                     required=False)):
        balance = Database.getDatabase().getUserMoney(interaction.user.id)[0]
        last_server_seed = None
        client_seed = interaction.user.id if client_seed is None else (
            client_seed[:32] if len(client_seed) > 32 else client_seed)
        server_seed, server_seed_hash = ProvablyFair.generate_server_seed()
        timestamp_hash = ProvablyFair.get_timestamp_hash()
        odds = 2.0
        win_profit = int(bet * (odds - 1))
        win_chance = round(95 / odds, 2)
        lo = int(100 * win_chance)
        hi = 10000 - lo
        view = self.HighLowView()
        await interaction.response.send_message(embed=Embed.getEmbed("HighLow",
                                                                     [("%user%",
                                                                       interaction.user.display_name),
                                                                      ("%user-icon-url%",
                                                                       interaction.user.avatar.url),
                                                                      ("%balance%", "{:,}".format(balance)),
                                                                      ("%bet%", "{:,}".format(bet)),
                                                                      ("%win-profit%", "{:,}".format(win_profit)),
                                                                      ("%jackpot-win%", "{:,}".format(bet * 5000)),
                                                                      ("%bet-odds%", odds),
                                                                      ("%win-chance%", win_chance), ("%lo%", lo),
                                                                      ("%hi%", hi),
                                                                      ("%server-seed-hash%", server_seed_hash),
                                                                      ("%client-seed%", client_seed),
                                                                      ("%timestamp-hash%", timestamp_hash),
                                                                      ("%last-server-seed%", last_server_seed)]),
                                                view=view)
        message: InteractionMessage = await interaction.original_message()
        while True:
            await view.wait()
            if view.action == "EditBet":
                balance = Database.getDatabase().getUserMoney(interaction.user.id)[0]
                back = False
                while not back:
                    edit_bet_view = self.EditBet(self.client, bet, balance)
                    await message.edit(embed=Embed.getEmbed("HighLow-EditBet",
                                                            [("%user%", interaction.user.display_name),
                                                             ("%user-icon-url%", interaction.user.avatar.url),
                                                             ("%bet%", "{:,}".format(bet)),
                                                             ("%win-profit%", "{:,}".format(int(bet * odds))),
                                                             ("%jackpot-win%", "{:,}".format(bet * 5000))]),
                                       view=edit_bet_view)
                    await edit_bet_view.wait()
                    bet = edit_bet_view.bet
                    back = edit_bet_view.back
            elif view.action == "SetOdds":
                messages = []
                msg = await self.client.wait_for("message", check=(lambda m: m.author == interaction.user), timeout=30)
                messages.append(msg)
                while not NumberUtils.isFloat(msg.content, lambda f: 1.01 <= f <= 4750):
                    a = await msg.reply("Invalid! Bet odds must be at least 1.01 and at most 4750!")
                    msg = await self.client.wait_for("message", check=(lambda m: m.author == interaction.user),
                                                     timeout=30)
                    messages.append(a)
                    messages.append(msg)
                await interaction.channel.delete_messages(messages)
                odds = round(float(msg.content), 2)
                win_chance = round(95 / odds, 2)
                win_profit = int(bet * (odds - 1))
                lo = int(100 * win_chance)
                hi = 10000 - lo
            elif view.action == "SetWinChance":
                messages = []
                msg = await self.client.wait_for("message", check=(lambda m: m.author == interaction.user), timeout=30)
                messages.append(msg)
                while not NumberUtils.isFloat(msg.content, lambda f: 0.02 <= f <= 94.06):
                    a = await msg.reply("Invalid! Win chance must be at least 0.02 and at most 94.06!")
                    msg = await self.client.wait_for("message", check=(lambda m: m.author == interaction.user),
                                                     timeout=30)
                    messages.append(a)
                    messages.append(msg)
                await interaction.channel.delete_messages(messages)
                win_chance = round(float(msg.content), 2)
                odds = round(95 / win_chance, 2)
                win_profit = int(bet * (odds - 1))
                lo = int(100 * win_chance)
                hi = 10000 - lo
            elif view.action == "SetClientSeed":
                msg = await self.client.wait_for("message", check=(lambda m: m.author == interaction.user), timeout=30)
                client_seed = msg.content[:32] if len(msg.content) > 32 else msg.content
                await msg.delete()
            if view.action:
                view = self.HighLowView()
                await message.edit(embed=Embed.getEmbed("HighLow",
                                                        [("%user%",
                                                          interaction.user.display_name),
                                                         ("%user-icon-url%",
                                                          interaction.user.avatar.url),
                                                         ("%bet%", "{:,}".format(bet)),
                                                         ("%balance%", "{:,}".format(balance)),
                                                         ("%win-profit%", "{:,}".format(win_profit)),
                                                         ("%jackpot-win%", "{:,}".format(bet * 5000)),
                                                         ("%bet-odds%", odds),
                                                         ("%win-chance%", win_chance), ("%lo%", lo),
                                                         ("%hi%", hi),
                                                         ("%server-seed-hash%", server_seed_hash),
                                                         ("%client-seed%", client_seed),
                                                         ("%timestamp-hash%", timestamp_hash),
                                                         ("%last-server-seed%", last_server_seed)]),
                                   view=view)
                await view.wait()
            Database.getDatabase().addUserMoney(interaction.user.id, -1 * bet, 0)
            balance -= bet
            secret = ProvablyFair.generate_number(server_seed, client_seed, timestamp_hash, 10000)
            last_server_seed = server_seed
            display = ''.join(emojis[int(i)] for i in str(secret))
            display = (5 - len(str(secret))) * emojis[0] + display
            if (view.value == "LO" and secret < lo) or (view.value == "HI" and secret > hi):
                balance += (win_profit + bet)
                await message.edit(embed=Embed.getEmbed("HighLowWon",
                                                        [("%user%",
                                                          interaction.user.display_name),
                                                         ("%user-icon-url%",
                                                          interaction.user.avatar.url),
                                                         ("%bet%", "{:,}".format(bet)),
                                                         ("%balance%", "{:,}".format(balance)),
                                                         ("%win-profit%", "{:,}".format(win_profit)),
                                                         ("%jackpot-win%", "{:,}".format(bet * 5000)),
                                                         ("%bet-odds%", odds),
                                                         ("%win-chance%", win_chance), ("%lo%", lo),
                                                         ("%hi%", hi),
                                                         ("%server-seed-hash%", server_seed_hash),
                                                         ("%client-seed%", client_seed),
                                                         ("%timestamp-hash%", timestamp_hash), ("%number%", display),
                                                         ("%bet-option%", view.value),
                                                         ("%last-server-seed%", last_server_seed)]),
                                   view=view)
                Database.getDatabase().addUserMoney(interaction.user.id, win_profit, 0)
            else:
                await message.edit(embed=Embed.getEmbed("HighLowLost",
                                                        [("%user%",
                                                          interaction.user.display_name),
                                                         ("%user-icon-url%",
                                                          interaction.user.avatar.url),
                                                         ("%bet%", "{:,}".format(bet)),
                                                         ("%balance%", "{:,}".format(balance)),
                                                         ("%win-profit%", "{:,}".format(win_profit)),
                                                         ("%jackpot-win%", "{:,}".format(bet * 5000)),
                                                         ("%bet-odds%", odds),
                                                         ("%win-chance%", win_chance), ("%lo%", lo),
                                                         ("%hi%", hi),
                                                         ("%server-seed-hash%", server_seed_hash),
                                                         ("%client-seed%", client_seed),
                                                         ("%timestamp-hash%", timestamp_hash), ("%number%", display),
                                                         ("%bet-option%", view.value),
                                                         ("%last-server-seed%", last_server_seed)]),
                                   view=view)
            view = self.HighLowView()
            await message.edit(view=view)
            server_seed, server_seed_hash = ProvablyFair.generate_server_seed()
            timestamp_hash = ProvablyFair.get_timestamp_hash()
            win_profit = int(bet * (odds - 1))
            win_chance = round(95 / odds, 2)
            lo = int(100 * win_chance)
            hi = 10000 - lo


def setup(client: Client):
    client.add_cog(HighLow(client))
