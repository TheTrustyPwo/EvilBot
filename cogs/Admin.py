from nextcord import slash_command, Client, Interaction, SlashOption, Member
from nextcord.ext import commands

from utils import Database, Embed

GUILD_IDS = [825894722324922438]


class Admin(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="money", description="Admin commands to manage user's money", guild_ids=GUILD_IDS)
    async def money(self, interaction: Interaction):
        """"""

    @money.subcommand(name="set", description="Set a user's money")
    async def money_set(self, interaction: Interaction,
                        user: Member = SlashOption(name="user", description="Specify the target", required=True),
                        walletAmount: int = SlashOption(name="wallet", description="Specify the wallet amount to set",
                                                        required=True),
                        bankAmount: int = SlashOption(name="bank", description="Specify the bank amount to set",
                                                      required=False)):
        bal, bank = Database.getDatabase().getUserMoney(user.id)
        bankAmount = bank if bankAmount is None else bankAmount
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
    client.add_cog(Admin(client))
