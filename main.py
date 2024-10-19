import nextcord
import os

from nextcord.ext import commands
from essentials import config
from essentials.logger import setup_logger
## from essentials import database

configurationManager = config.ConfigurationManager()
defaultConfig = configurationManager.getBotConfig()

## Intents
# """Would recommend to enable on the bot panel. Configure as required."""
intents = nextcord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.guilds = True

## Bot Construction

bot = commands.Bot(intents=intents)
logger = setup_logger()

for filename in os.listdir(
    "./ext"
):  # Use ./ext as a folder to contain all Cogs (Commands)
    if filename.endswith(".py"):
        bot.load_extension(f"ext.{filename[:-3]}")
        logger.info(f"""Loading extension ext.{filename[:-3]}...""")


@bot.event
async def on_ready():
    logger.info(f"Running OpenRewards Release Version - {defaultConfig['RELEASE']}")  


bot.run(defaultConfig["BOT-TOKEN"])
