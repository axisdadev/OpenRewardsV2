import nextcord
import essentials.formats.JSONFormatter as jsonFormatter

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

        if loadCommandConfig is False:
            useDefaultConfig = True  # noqa: F841
            pass

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
            jsonFromYML = loadCommandConfig["EMBED_JSON"]
            variables = jsonFormatter.extractVariables(jsonFromYML)

            for customVariable, value in customVariables.items():
                if customVariable in variables:
                    jsonFromYML = jsonFormatter.replaceVariables(
                        jsonFromYML, {customVariable: value}
                    )

            jsonToEmbed = jsonFormatter.jsonToEmbed(json_string=jsonFromYML)
            await interaction.send(embed=jsonToEmbed)


def setup(bot):
    bot.add_cog(Util(bot))
