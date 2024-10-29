import nextcord
import nextcord.utils
import essentials.formats.JSONFormatter as jsonFormatter
import essentials.botUtils.permissionChecks as permissionChecks
import essentials.botUtils.design as design

from nextcord.ext import commands
from nextcord import Embed
from essentials import database, config, variableReference
from essentials.logger import setup_logger


class Util(commands.Cog, name="util"):
    """A bunch of utility commands for your OpenRewards bot."""

    def __init__(self, bot):
        self.bot = bot
        self.preloadedDatabaseManager = database.DatabaseManager()
        self.botConfigManager = config.ConfigurationManager()
        self.botConfig = self.botConfigManager.getBotConfig()
        self.log = setup_logger()

    @nextcord.slash_command()
    async def ping(self, interaction: nextcord.Interaction):
        """Returns the latency of the bot."""
        loadCommandConfig = self.botConfigManager.getCommandConfig("ping", check=False)
        useDefaultConfig = False
        customVariables = {"bot.ping": round(self.bot.latency * 1000)}

        if loadCommandConfig is False or loadCommandConfig["CUSTOM-RESPONSE"] is False:
            useDefaultConfig = True  # noqa: F841
            pass

        if loadCommandConfig and loadCommandConfig["PERMS-REQUIRED"] is True:
            roleCheck = permissionChecks.has_roles(
                member=interaction.user, roles=loadCommandConfig["ADDITIONAL-ROLES"]
            )

            if not roleCheck:
                await interaction.send(
                    embed=design.Embeds.invalidPermissionEmbed, ephemeral=True
                )
                return

        if useDefaultConfig:
            responseEmbed = Embed(
                title="🏓 Pong!", colour=nextcord.Color(int("3DED97", 16))
            )
            responseEmbed.add_field(
                name="My latency is...",
                inline=True,
                value=f"```{round(self.bot.latency * 1000)}ms!```",
            )

            await interaction.send(embed=responseEmbed)
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


def setup(bot):
    bot.add_cog(Util(bot))
