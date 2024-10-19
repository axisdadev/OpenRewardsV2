import yaml

from essentials.logger import setup_logger


class ConfigurationManager:
    def __init__(self):
        with open("configurations/bot.yml") as f:
            yamlFile = yaml.safe_load(f)
            self.botConfig = yamlFile
            self.log = setup_logger()

        return

    def getBotConfig(self):
        """Get the default configuration set for the bot upon launch."""
        return self.botConfig

    def getCommandConfig(self, name: str, check: bool):
        """Get a configuration for a specific command. Must be a valid configuration file name matching command to register"""

        filePath = f"configurations/commands/{name}.yml"
        result = None

        try:
            with open(file=filePath) as f:
                yamlFile = yaml.safe_load(f)
                result = yamlFile
        except Exception:
            if not check:
                self.log.warning(
                    f"""Unable to find configuration file "{name}.yml, Will default to normal."""
                )
            return False

        return result
