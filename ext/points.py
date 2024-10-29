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
            embedsList = design.Embeds()
            embedWithReason = embedsList.invalidPermissionEmbed
            await interaction.send(embed=embedWithReason, ephemeral=True)
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
                "points.changed": points,
            }

            if useDefaultConfig:
                responseEmbed = Embed(
                    title="Points Added",
                    description="Congratulations, new points have been added to your account!",
                )
                responseEmbed.add_field(
                    name="Points",
                    value=f"```{updatedProfileData["points"]}```",
                    inline=True,
                )
                responseEmbed.add_field(
                    name="Points Added", value=f"```{points}```", inline=True
                )

                await interaction.send(embed=responseEmbed)
                return
            else:
                jsonPath = loadCommandConfig["EMBED_PATH"]
                jsonLoaded = jsonFormatter.loadEmbedData(jsonPath)
                jsonToEmbedReferences = await jsonFormatter.jsonToEmbedAddReferences(
                    jsonLoaded, interaction, customVariables
                )

                await interaction.send(
                    content=await variableReference.replace_references(
                        loadCommandConfig["CONTENT"], interaction, customVariables
                    ),
                    embed=jsonToEmbedReferences,
                )
                return

            pass
        else:
            await interaction.send(embed=design.Embeds.errorEmbed, ephemeral=True)
            return

        return
    
    @nextcord.slash_command()
    async def remove(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = SlashOption(
            description="The user to remove rewards from.", required=True
        ),
        points: int = SlashOption(
            description="The amount of points or rewards to remove from a user.",
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

        if points > self.botConfig["MAX-SUB"] and not adminPermissionCheck:
            embedsList = design.Embeds()
            embedWithReason = embedsList.invalidPermissionEmbed
            await interaction.send(embed=embedWithReason, ephemeral=True)
            return

        loadCommandConfig = self.botConfigManager.getCommandConfig("add", check=False)
        useDefaultConfig = False

        if loadCommandConfig is False or loadCommandConfig["CUSTOM-RESPONSE"] is False:
            useDefaultConfig = True  # noqa: F841
            pass

        if points > fetchProfile["points"] and not adminPermissionCheck:
            embedsList = design.Embeds()
            embedWithReason = embedsList.invalidPermissionEmbed
            embedWithReason.description + " | User has insufficent points"

            await interaction.send(embed=embedWithReason, ephemeral=True)
            return 

        updateStatement = await self.preloadedDatabaseManager.updateProfile(
            discordId=user.id, update={"points": int(fetchProfile["points"]) - points}
        )

        updatedProfileData = await self.preloadedDatabaseManager.fetchProfile(
            discordId=user.id
        )

        if updateStatement:
            customVariables = {
                "points.previous": fetchProfile["points"],
                "points.current": updatedProfileData["points"],
                "points.changed": points,
            }

            if useDefaultConfig:
                responseEmbed = Embed(
                    title="Points Remove",
                    description="Points have been removed from user account.",
                )
                responseEmbed.add_field(
                    name="Points",
                    value=f"```{updatedProfileData["points"]}```",
                    inline=True,
                )
                responseEmbed.add_field(
                    name="Points Removed", value=f"```{points}```", inline=True
                )

                await interaction.send(embed=responseEmbed)
                return
            else:
                jsonPath = loadCommandConfig["EMBED_PATH"]
                jsonLoaded = jsonFormatter.loadEmbedData(jsonPath)
                jsonToEmbedReferences = await jsonFormatter.jsonToEmbedAddReferences(
                    jsonLoaded, interaction, customVariables
                )

                await interaction.send(
                    content=await variableReference.replace_references(
                        loadCommandConfig["CONTENT"], interaction, customVariables
                    ),
                    embed=jsonToEmbedReferences,
                )
                return

            pass
        else:
            await interaction.send(embed=design.Embeds.errorEmbed, ephemeral=True)
            return

        return


    @nextcord.slash_command()
    async def stats(self, interaction: nextcord.Interaction, user: nextcord.Member):
        return


def setup(bot):
    bot.add_cog(Points(bot))
