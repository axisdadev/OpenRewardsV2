from asynctinydb import TinyDB
import config


class DatabaseManager:
    def __init__(self):
        configurationManager = config.configurationManager()
        defaultConfig = configurationManager.getBotConfig()

        self.Database = TinyDB(defaultConfig['DEFAULT-DATABASE'])
        pass
    