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
):  # Use ./ext as a folder to contain all Cogs (Command Groups)
    if filename.endswith(".py"):
        bot.load_extension(f"ext.{filename[:-3]}")
        logger.info(f"""Loaded extension ext.{filename[:-3]}!""")


## Database check / Creation

if not os.path.exists(defaultConfig["DEFAULT-DATABASE"]):
    with open(defaultConfig["DEFAULT-DATABASE"], mode="a+") as newDB:
        logger.info("Created a new database based of bot.yml, Since it didn't exist previously.")
        pass

if not os.path.exists(defaultConfig["BACKUP-DATABASE"]) and defaultConfig["ENABLE-BACKUP"]:
    with open(defaultConfig["BACKUP-DATABASE"], mode="a+") as newDB:
        logger.info("Created a new backup database based of bot.yml, Since it didn't exist previously.")
        pass

 
@bot.event
async def on_ready():
    logger.info(f"Running OpenRewards Release Version - {defaultConfig['RELEASE']}")


bot.run(defaultConfig["BOT-TOKEN"])