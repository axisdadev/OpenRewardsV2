from asynctinydb import TinyDB, Query
from essentials import config
from essentials.logger import setup_logger
import uuid


class DatabaseManager:
    def __init__(self):
        configurationManager = config.ConfigurationManager()
        defaultConfig = configurationManager.getBotConfig()

        self.Database = TinyDB(defaultConfig["DEFAULT-DATABASE"])
        self.log = setup_logger()
        pass

    async def createProfile(self, discordId: str):
        check = await self.fetchProfile(discordId)

        if check is not False:
            self.log.warning(
                f"""Failed to create Profile with a discordID of {discordId}, Already is present in Database"""
            )
            return False

        action = await self.Database.insert(
            document={
                "discordId": discordId,
                "points": 0,
                "itemsOwned": {},
                "UUID": str(object=uuid.uuid4()),
            }
        )

        if action:
            self.log.info(f"""Profile created with a discordID of {discordId}""")
            return action
        else:
            self.log.warning(
                f"""Failed to create profile created with a discordID of {discordId}"""
            )
            return False

    async def fetchProfile(self, discordId: str):
        configurationManager = config.ConfigurationManager()
        defaultConfig = configurationManager.getBotConfig()
        localDatabase = TinyDB(defaultConfig["DEFAULT-DATABASE"])

        search = Query()
        profile = await localDatabase.get(search.discordId == discordId)

        if profile:
            return profile
        elif not profile:
            self.log.warning(
                f"""Failed to fetch profile with a discordID of {discordId}"""
            )
            return False

    async def updateProfile(self, discordId: str, update: dict):
        configurationManager = config.ConfigurationManager()
        defaultConfig = configurationManager.getBotConfig()
        localDatabase = TinyDB(defaultConfig["DEFAULT-DATABASE"])

        search = Query()
        updateStatement = await localDatabase.update(
            update, search.discordId == discordId
        )

        if updateStatement:
            return True
        elif not updateStatement:
            self.log.warning(
                f"""Failed to update profile with a discordID of {discordId}"""
            )
            return False
