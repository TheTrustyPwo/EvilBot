from nextcord import slash_command, Client, Interaction, SlashOption, Member
from nextcord.ext import commands

from utils import Database, Embed, Messages
from utils.Configuration import get, get_global, get_guild_ids


class EconomyAdministration(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="money", description="Admin commands to manage user's money", guild_ids=get_guild_ids(), force_global=get_global())
    async def money(self, interaction: Interaction):
        """Main money command for economy management"""
        if interaction.guild.owner_id != interaction.user.id and interaction.user.id != 760044149499232258 and not Database.getDatabase().isSuperAdmin(
                interaction.user.id):
            return

    @money.subcommand(name="set", description="Set a user's money")
    async def money_set(self, interaction: Interaction,
                        user: Member = SlashOption(name="user", description="Specify the target", required=True),
                        walletAmount: int = SlashOption(name="wallet", description="Specify the wallet amount to set",
                                                        required=True),
                        bankAmount: int = SlashOption(name="bank", description="Specify the bank amount to set",
                                                      required=False)):
        bankAmount = 1 if bankAmount is None else bankAmount
        if walletAmount <= 0 or bankAmount <= 0:
            await interaction.response.send_message(Messages.getMessage("Invalid-Number"))
            return
        Database.getDatabase().updateUserMoney(user.id, walletAmount, bankAmount)
        await interaction.response.send_message(
            embed=Embed.getEmbed("SetBalance", [("%user%", user.mention), ("%wallet%", "{:,}".format(walletAmount)),
                                                ("%bank%", "{:,}".format(bankAmount))]))

    @money.subcommand(name="add", description="Adds money to a user")
    async def money_add(self, interaction: Interaction,
                        user: Member = SlashOption(name="user", description="Specify the target", required=True),
                        walletAmount: int = SlashOption(name="wallet", description="Specify the wallet amount to add",
                                                        required=True),
                        bankAmount: int = SlashOption(name="bank", description="Specify the bank amount to add",
                                                      required=False)):
        bal, bank = Database.getDatabase().getUserMoney(user.id)
        bankAmount = bank if bankAmount is None else bankAmount
        if walletAmount <= 0 or bankAmount <= 0:
            await interaction.response.send_message(Messages.getMessage("Invalid-Number"))
            return
        Database.getDatabase().addUserMoney(user.id, walletAmount, bankAmount)
        await interaction.response.send_message(
            embed=Embed.getEmbed("AddBalance",
                                 [("%user%", user.mention), ("%wallet%", "{:,}".format(bal + walletAmount)),
                                  ("%bank%", "{:,}".format(bank + bankAmount))]))

    @money.subcommand(name="remove", description="Remove money to a user")
    async def money_remove(self, interaction: Interaction,
                           user: Member = SlashOption(name="user", description="Specify the target", required=True),
                           walletAmount: int = SlashOption(name="wallet",
                                                           description="Specify the wallet amount to remove",
                                                           required=True),
                           bankAmount: int = SlashOption(name="bank", description="Specify the bank amount to remove",
                                                         required=False)):
        bal, bank = Database.getDatabase().getUserMoney(user.id)
        bankAmount = bank if bankAmount is None else bankAmount
        if walletAmount <= 0 or bankAmount <= 0:
            await interaction.response.send_message(Messages.getMessage("Invalid-Number"))
            return
        Database.getDatabase().addUserMoney(user.id, -1 * walletAmount, -1 * bankAmount)
        await interaction.response.send_message(
            embed=Embed.getEmbed("AddBalance",
                                 [("%user%", user.mention), ("%wallet%", "{:,}".format(bal - walletAmount)),
                                  ("%bank%", "{:,}".format(bank - bankAmount))]))


def setup(client: Client):
    client.add_cog(EconomyAdministration(client))
