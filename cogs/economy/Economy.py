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


    @slash_command(name="search", description="Search different places in hopes of finding money", guild_ids=get_guild_ids(), force_global=get_global())
    async def search(self, interaction: Interaction):
        cooldown, timeLeft = Database.getDatabase().isOnCooldown(interaction.user.id, "search")
        if cooldown:
            await interaction.response.send_message(f"ON COOLDOWN {timeLeft - int(time.time())} SECONDS LEFT")
            return
        Database.getDatabase().createCooldown(interaction.user.id, "search", 10)


def setup(client: Client):
    client.add_cog(Economy(client))
