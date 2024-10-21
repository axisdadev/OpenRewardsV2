import nextcord
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

        ref = await variableReference.get_reference(variable="user.points", interaction=interaction, additionalParams={})
        print(ref)

        
        if loadCommandConfig is False:
            useDefaultConfig = True  # noqa: F841
            pass

        if useDefaultConfig:
            responseEmbed = Embed(title="🏓 Pong!", colour=nextcord.Color(int("3DED97", 16)))
            responseEmbed.add_field(name="My latency is...", inline=True, value=f"```{round(self.bot.latency * 1000)}ms!```")

            await interaction.send(embed=responseEmbed)
        else:
            return NotImplemented

        



        


    

def setup(bot):
    bot.add_cog(Util(bot))

    



