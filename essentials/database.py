from asynctinydb import TinyDB, Query
from nextcord.ext import tasks
from essentials import config
from essentials.logger import setup_logger
import uuid
import json
import time
import os

defaultConfig = config.ConfigurationManager().getBotConfig()


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

    @tasks.loop(minutes=defaultConfig["BACKUP-MINUTES"])
    async def backupDatabase(self):
        if defaultConfig["ENABLE-BACKUP"] is True:
            self.log.info("Backing up database...")

            try:
                start = int(time.time())

                fileSizeCheck = os.path.getsize(defaultConfig["DEFAULT-DATABASE"])
                if fileSizeCheck == 0:
                    self.log.warning(f"Unable to backup data. No data is in {defaultConfig["DEFAULT-DATABASE"]} Heed this warning.")
                    return
                
                with open(
                    file=f"{defaultConfig["DEFAULT-DATABASE"]}", mode="r"
                ) as source:
                    data = json.load(fp=source)

                with open(
                    file=f"{defaultConfig["BACKUP-DATABASE"]}", mode="w"
                ) as destination:
                    json.dump(data, destination, indent=None)

                end = int(time.time())
                self.log.info(
                    f"Sucessfully backed up data! Took {end-start}ms"
                )
            except Exception as e:
                self.log.warning(f"Unable to backup data. Exception: {e}")

        return
