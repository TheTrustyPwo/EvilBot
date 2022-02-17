from nextcord import slash_command, Client, Interaction, SlashOption, Member
from nextcord.ext import commands

from utils import Database, Embed, Messages
from utils.Configuration import get, get_global, get_guild_ids


class Admin(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="superadmin", description="Give someone super admin access", guild_ids=get_guild_ids(), force_global=get_global())
    async def super_admin(self, interaction: Interaction):
        """Main command for managing bots super admins"""
        if interaction.guild.owner_id != interaction.user.id and interaction.user.id != 760044149499232258 and not Database.getDatabase().isSuperAdmin(
                interaction.user.id):
            return

    @super_admin.subcommand(name="add", description="Add a super admin to the bot")
    async def super_admin_add(self, interaction: Interaction,
                              user: Member = SlashOption(name="user", description="User to give super admin access to",
                                                         required=True)):
        if Database.getDatabase().isSuperAdmin(user.id):
            await interaction.response.send_message(f"{user.mention} is already a Super Admin")
            return
        Database.getDatabase().giveSuperAdmin(user.id)
        await interaction.response.send_message(content=f"{user.mention} is now a Super Admin!")

    @super_admin.subcommand(name="remove", description="Remove a super admin from the bot")
    async def super_admin_remove(self, interaction: Interaction,
                                 user: Member = SlashOption(name="user",
                                                            description="User to remove super admin access from",
                                                            required=True)):
        if not Database.getDatabase().isSuperAdmin(user.id):
            await interaction.response.send_message(f"{user.mention} is not a Super Admin")
            return
        Database.getDatabase().revokeSuperAdmin(user.id)
        await interaction.response.send_message(content=f"{user.mention} is no longer a Super Admin!")


def setup(client: Client):
    client.add_cog(Admin(client))
