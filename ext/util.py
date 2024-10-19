import nextcord
from nextcord.ext import commands
from essentials import database, config
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
    async def hello(self, ctx, *, member: nextcord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member
    

def setup(bot):
    ## Run checks for configuration in each command
    bot.add_cog(Util(bot))

    tempLog = setup_logger()
    cog = bot.get_cog("util")

    tempLog.info(f"> Loaded ext.{cog.qualified_name}!")

    



