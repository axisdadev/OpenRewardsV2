import nextcord
import nextcord.utils

import essentials.formats.JSONFormatter as jsonFormatter
import essentials.botUtils.permissionChecks as permissionChecks
import essentials.botUtils.design as design

from nextcord.ext import commands
from nextcord import SlashOption, Embed
from essentials import database, config, variableReference
from essentials.logger import setup_logger


class Points(commands.Cog, name="points"):
    """The cog for managing user points. Make sure to set staff permissions for each command in configurations/commands"""

    def __init__(self, bot):
        self.bot = bot
        self.preloadedDatabaseManager = database.DatabaseManager()
        self.botConfigManager = config.ConfigurationManager()
        self.botConfig = self.botConfigManager.getBotConfig()
        self.log = setup_logger()

    @nextcord.slash_command()
    async def add(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to give rewards to.", required=True
        ),
        points: int = SlashOption(
            description="The amount of points or rewards to give to a user.",
            required=True,
        ),
    ):
        fetchProfile = await self.preloadedDatabaseManager.fetchProfile(
            discordId=user.id
        )
        if not fetchProfile:
            createProfile = await self.preloadedDatabaseManager.createProfile(
                discordId=user.id
            )
            if createProfile:
                fetchProfile = await self.preloadedDatabaseManager.fetchProfile(
                    discordId=user.id
                )

        staffRoles = self.botConfig["STAFF-ROLES"]
        adminRoles = self.botConfig["ADMIN-ROLES"]

        staffPermissionCheck = permissionChecks.has_roles(member=user, roles=staffRoles)
        adminPermissionCheck = permissionChecks.has_roles(member=user, roles=adminRoles)

        if not staffPermissionCheck or adminPermissionCheck:
            await interaction.send(
                embed=design.Embeds.invalidPermissionEmbed, ephemeral=True
            )
            return

        if points > self.botConfig["MAX-ADD"] and not adminPermissionCheck:
            embedWithReason = design.Embeds.invalidPermissionEmbed
            embedWithReason.description = (
                embedWithReason.description
                + f" | You can not add more points then the set limit of **{self.botConfig["MAX-ADD"]}**"
            )
            await interaction.send(
                embed=design.Embeds.invalidPermissionEmbed, ephemeral=True
            )
            return

        loadCommandConfig = self.botConfigManager.getCommandConfig("add", check=False)
        useDefaultConfig = False

        if loadCommandConfig is False or loadCommandConfig["CUSTOM-RESPONSE"] is False:
            useDefaultConfig = True  # noqa: F841
            pass

        updateStatement = await self.preloadedDatabaseManager.updateProfile(
            discordId=user.id, update={"points": int(fetchProfile["points"]) + points}
        )

        updatedProfileData = await self.preloadedDatabaseManager.fetchProfile(
            discordId=user.id
        )

        if updateStatement:
            customVariables = {
                "points.previous": fetchProfile["points"],
                "points.current": updatedProfileData["points"],
            }

            if useDefaultConfig:
                pass
            else:
                return

            pass
        else:
            await interaction.send(embed=design.Embeds.errorEmbed, ephemeral=True)
            return 

        return

    @nextcord.slash_command()
    async def remove(
        self, interaction: nextcord.Interaction, user: nextcord.Member, points: int
    ):
        return

    @nextcord.slash_command()
    async def stats(self, interaction: nextcord.Interaction, user: nextcord.Member):
        return


def setup(bot):
    bot.add_cog(Points(bot))
