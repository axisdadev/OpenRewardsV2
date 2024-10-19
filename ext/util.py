import nextcord
from nextcord import Interaction, Embed
from nextcord.ext import commands
from essentials import database, config


class Util(commands.Cog):
    """A bunch of utility commands for your OpenRewards bot."""

    def __init__(self, bot):
        self.bot = bot
        self.preloadedDatabaseManager = database.DatabaseManager()
        self.botConfigManager = config.ConfigurationManager()
        self.botConfig = self.botConfigManager.getBotConfig()


def setup(bot):
    ## Run checks for configuration in each command

    
    bot.add_cog(Util(bot))
