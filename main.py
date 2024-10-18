import nextcord
import logging
import os

from nextcord.ext import commands
from essentials import config
from essentials import database

configurationManager = config.ConfigurationManager()
defaultConfig = configurationManager.getBotConfig()

## Intents
# """Would recommend to enable on the bot panel. Configure as required."""
intents = nextcord.Intents.default()
intents.message_content = True
intents.dm_messages = True
intents.guilds = True

## Logging

if defaultConfig["LOGGING"] is True:
    logger = logging.getLogger("nextcord")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(defaultConfig["LOG-FILE"])
    handler.setFormatter(
        fmt=logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    logger.addHandler(handler)


## Bot Construction

bot = commands.Bot(intents=intents)

for filename in os.listdir(
    "./ext"
):  # Use ./ext as a folder to contain all Cogs (Commands)
    if filename.endswith(".py"):
        bot.load_extension(f"ext.{filename[:-3]}")


@bot.event
async def on_ready():
    print(
        f"Running OpenRewards Release Version - {defaultConfig['RELEASE']}\nThank you for using OpenRewards!"
    )


bot.run(defaultConfig["BOT-TOKEN"])
