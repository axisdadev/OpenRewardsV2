import yaml
import os

from essentials.logger import setup_logger


class ConfigurationManager:
    def __init__(self):
        with open("configurations/bot.yml") as f:
            yamlFile = yaml.safe_load(f)
            self.botConfig = yamlFile
            self.log = setup_logger()
            self.warnings = []

        return

    def getBotConfig(self):
        """Get the default configuration set for the bot upon launch."""
        return self.botConfig

    def getCommandConfig(self, name: str, check: bool):
        """Get a configuration for a specific command. Must be a valid configuration file name matching command to register"""

        filePath = os.path.join(f"configurations/commands/{name}.yml")
        result = None

        try:
            with open(file=filePath, mode="r") as f:
                yamlFile = yaml.safe_load(f)
                result = yamlFile
        except Exception as e:
            if not check:
                if name not in self.warnings:
                    if e is FileNotFoundError:
                        self.log.warning(
                            f"""Unable to find configuration file "{name}.yml", Will default to normal."""
                        )
                    else:
                        self.log.warning(
                            f"""Unable to find access configuration file with Exception being: "{e}" """
                        )

                    self.warnings.append(name)

            return False

        return result
