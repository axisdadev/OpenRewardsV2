import nextcord, os, logging
from nextcord.ext import commands
from essentials import config

configurationManager = config.ConfigurationManager()
defaultConfig = configurationManager.getBotConfig()

