from asynctinydb import TinyDB, UUID, Query
import config


class DatabaseManager:
    def __init__(self):
        configurationManager = config.configurationManager()
        defaultConfig = configurationManager.getBotConfig()

        self.Database = TinyDB(defaultConfig["DEFAULT-DATABASE"])
        pass

    async def createProfile(self, discordId: str):
        action = await self.Database.insert(
            document={
                "discordId": discordId,
                "points": 0,
                "itemsOwned": {},
                "UUID": UUID(),
            }
        )

        if action:
            print(f"""Profile created with a discordID of {discordId}""")
            return action
        else:
            print(
                f"""Failed to create profile created with a discordID of {discordId}"""
            )
            return False

    async def fetchProfile(self, discordId: str):
        configurationManager = config.configurationManager()
        defaultConfig = configurationManager.getBotConfig()
        localDatabase = TinyDB(defaultConfig["DEFAULT-DATABASE"])

        search = Query()
        profile = localDatabase.get(search.discordId == discordId)

        if profile:
            return profile
        else:
            print(
                f"""Failed to fetch profile created with a discordID of {discordId}"""
            )
            return False
