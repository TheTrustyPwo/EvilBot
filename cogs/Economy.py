import random
import time

import nextcord
from nextcord import slash_command, Interaction, Client, SlashOption, Member, InteractionMessage
from nextcord.ext import commands

from utils import Database, Embed, Messages, ProvablyFair
from utils.Configuration import get, get_global, get_guild_ids


class Economy(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="balance", description="Checks a user's balance", guild_ids=get_guild_ids(), force_global=get_global())
    async def balance(self, interaction: Interaction,
                      user: Member = SlashOption(name="user", description="Specify the user to check their balance",
                                                 required=False)):
        user = interaction.user if user is None else user
        bal, bank = Database.getDatabase().getUserMoney(user.id)
        await interaction.response.send_message(embed=Embed.getEmbed(
            "Balance",
            [("%user%", user.display_name), ("%balance%", "{:,}".format(bal)), ("%bank%", "{:,}".format(bank))]))

    @slash_command(name="deposit", description="Deposit money into your bank", guild_ids=get_guild_ids(), force_global=get_global())
    async def deposit(self, interaction: Interaction,
                      amount: int = SlashOption(name="amount", description="The amount you want to deposit",
                                                required=True, autocomplete=True, default=1)):
        if not amount:
            return
        amount = int(amount)
        bal, bank = Database.getDatabase().getUserMoney(interaction.user.id)
        if amount <= 0:
            await interaction.response.send_message(Messages.getMessage("Invalid-Number"))
            return
        if amount > bal:
            await interaction.response.send_message(
                Messages.getMessage("Deposit-No-Money", [("%balance%", "{:,}".format(bal))]))
            return
        Database.getDatabase().addUserMoney(interaction.user.id, -1 * amount, amount)
        await interaction.response.send_message(
            embed=Embed.getEmbed("Deposit", [("%user%", interaction.user.display_name),
                                             ("%balance%",
                                              "{:,}".format(-1 * amount + bal)),
                                             ("%bank%",
                                              "{:,}".format(amount + bank))]))

    @deposit.on_autocomplete("amount")
    async def deposit_autocomplete(self, interaction: Interaction, amount: int):
        await interaction.response.send_autocomplete([Database.getDatabase().getUserMoney(interaction.user.id)[0]])

    @slash_command(name="withdraw", description="Withdraws your money from the bank", guild_ids=get_guild_ids(), force_global=get_global())
    async def withdraw(self, interaction: Interaction,
                       amount: int = SlashOption(name="amount", description="The amount you want to withdraw",
                                                 required=True, autocomplete=True, default=1)):
        bal, bank = Database.getDatabase().getUserMoney(interaction.user.id)
        if amount <= 0:
            await interaction.response.send_message(Messages.getMessage("Invalid-Number"))
            return
        if amount > bank:
            await interaction.response.send_message(
                Messages.getMessage("Withdraw-No-Money", [("%bank%", "{:,}".format(bank))]))
            return
        Database.getDatabase().addUserMoney(interaction.user.id, amount, -1 * amount)
        await interaction.response.send_message(
            embed=Embed.getEmbed("Withdraw", [("%user%", interaction.user.display_name),
                                              ("%balance%", "{:,}".format(amount + bal)),
                                              ("%bank%", "{:,}".format(-1 * amount + bank))]))

    @withdraw.on_autocomplete("amount")
    async def withdraw_autocomplete(self, interaction: Interaction, amount: int):
        await interaction.response.send_autocomplete([Database.getDatabase().getUserMoney(interaction.user.id)[1]])

    @slash_command(name="beg", description="Beg strangers for money", guild_ids=get_guild_ids(), force_global=get_global())
    async def beg(self, interaction: Interaction):
        cooldown, timeLeft = Database.getDatabase().isOnCooldown(interaction.user.id, "beg")
        if cooldown:
            await interaction.response.send_message(f"ON COOLDOWN {timeLeft - int(time.time())} SECONDS LEFT")
            return
        Database.getDatabase().createCooldown(interaction.user.id, "beg", 10)
        success = random.choices([True, False], weights=[50, 50], k=1)[0]
        if success:
            amount = random.randint(600, 1000)
            Database.getDatabase().addUserMoney(interaction.user.id, amount, 0)
            await interaction.response.send_message(
                embed=Embed.getEmbed("SuccessBeg", [("%name%", random.choice(interaction.guild.members).display_name),
                                                    ("%message%", Messages.getMessage("Begging-Success", [
                                                        ("%amount%", "{:,}".format(amount))]))]))
        else:
            await interaction.response.send_message(
                embed=Embed.getEmbed("FailureBeg", [("%name%", random.choice(interaction.guild.members).display_name),
                                                    ("%message%", Messages.getMessage("Begging-Failure"))]))

    @slash_command(name="pay", description="Send money to someone quickly", guild_ids=get_guild_ids(), force_global=get_global())
    async def pay(self, interaction: Interaction,
                  user: Member = SlashOption(name="user", description="The user to pay", required=True),
                  amount: int = SlashOption(name="amount", description="The amount to pay", required=True)):
        bal, bank = Database.getDatabase().getUserMoney(interaction.user.id)
        if amount <= 0:
            await interaction.response.send_message(Messages.getMessage("Invalid-Number"))
            return
        if amount > bal:
            await interaction.response.send_message(
                Messages.getMessage("Withdraw-No-Money", [("%bank%", "{:,}".format(bank))]))
            return
        Database.getDatabase().addUserMoney(interaction.user.id, -1 * amount, 0)
        Database.getDatabase().addUserMoney(user.id, amount, 0)
        receiverBal, receiverBank = Database.getDatabase().getUserMoney(user.id)
        await interaction.response.send_message(embed=Embed.getEmbed("Pay", [("%shared%", "{:,}".format(amount)), (
            "%your-wallet%", "{:,}".format(bal - amount)), ("%receiver%", user.display_name), ("%receiver-wallet%",
                                                                                               "{:,}".format(
                                                                                                   receiverBal))]))

    class HighLow(nextcord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @nextcord.ui.button(label="Lower", style=nextcord.ButtonStyle.primary)
        async def lower(self, button: nextcord.ui.Button, interaction: Interaction):
            self.value = "Lower"
            self.stop()

        @nextcord.ui.button(label="JACKPOT", style=nextcord.ButtonStyle.primary)
        async def jackpot(self, button: nextcord.ui.Button, interaction: Interaction):
            self.value = "Jackpot"
            self.stop()

        @nextcord.ui.button(label="Higher", style=nextcord.ButtonStyle.primary)
        async def higher(self, button: nextcord.ui.Button, interaction: Interaction):
            self.value = "Higher"
            self.stop()

        @nextcord.ui.button(label="❓ How it works?", style=nextcord.ButtonStyle.green)
        async def howItWorks(self, button: nextcord.ui.button, interaction: Interaction):
            await interaction.response.send_message(Messages.getMessage("HighLow-HowItWorks"), ephemeral=True)

    @slash_command(name="highlow", description="Bet on the high-low game!", guild_ids=get_guild_ids(), force_global=get_global())
    async def highlow(self, interaction: Interaction,
                      bet: int = SlashOption(name="bet", description="How much you want to bet", required=True),
                      client_seed: str = SlashOption(name="client_seed", description="Specify your client seed",
                                                     required=False)):
        client_seed = interaction.user.id if client_seed is None else (
            client_seed[:32] if len(client_seed) > 32 else client_seed)
        server_seed, server_seed_hash = ProvablyFair.generate_server_seed()
        minimum = get()["Economy"]["HighLow"]["Min-Value"]
        maximum = get()["Economy"]["HighLow"]["Max-Value"]
        number = random.randint(minimum, maximum)
        view = self.HighLow()
        await interaction.response.send_message(embed=Embed.getEmbed("HighLow",
                                                                     [("%user%",
                                                                       interaction.user.display_name),
                                                                      ("%user-icon-url%",
                                                                       interaction.user.avatar.url),
                                                                      ("%min%", minimum), ("%max%", maximum),
                                                                      ("%number%", number)]),
                                                view=view)
        message: InteractionMessage = await interaction.original_message()
        await view.wait()
        secret = ProvablyFair.generate_number(server_seed, client_seed, ProvablyFair.get_timestamp_hash(), maximum)
        if (view.value == "Lower" and secret < number) or (view.value == "Higher" and secret > number):
            await message.edit(embed=Embed.getEmbed("HighLowWon",
                                                    [("%user%", interaction.user.display_name),
                                                     ("%user-icon-url%", interaction.user.avatar.url),
                                                     ("%hint%", number), ("%number%", secret),
                                                     ("%amount%", "{:,}".format(bet))]))
            Database.getDatabase().addUserMoney(interaction.user.id, bet, 0)
        elif view.value == "Jackpot" and secret == number:
            await interaction.response.send_message("JACKPOT!!!")
        else:
            await message.edit(embed=Embed.getEmbed("HighLowLost",
                                                    [("%user%", interaction.user.display_name),
                                                     ("%user-icon-url%", interaction.user.avatar.url),
                                                     ("%hint%", number), ("%number%", secret)]))
            Database.getDatabase().addUserMoney(interaction.user.id, -1 * bet, 0)

    @slash_command(name="search", description="Search different places in hopes of finding money", guild_ids=get_guild_ids(), force_global=get_global())
    async def search(self, interaction: Interaction):
        cooldown, timeLeft = Database.getDatabase().isOnCooldown(interaction.user.id, "search")
        if cooldown:
            await interaction.response.send_message(f"ON COOLDOWN {timeLeft - int(time.time())} SECONDS LEFT")
            return
        Database.getDatabase().createCooldown(interaction.user.id, "search", 10)


def setup(client: Client):
    client.add_cog(Economy(client))
