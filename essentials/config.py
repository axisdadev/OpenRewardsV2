import yaml


class ConfigurationManager:
    def __init__(self):
        with open("configurations/bot.yml") as f:
            yamlFile = yaml.safe_load(f)
            self.botConfig = yamlFile

        return

    def getBotConfig(self):
        """Get the default configuration set for the bot upon launch."""
        return self.botConfig

    def getCommandConfig(self, name):
        """Get a configuration for a specific command. Must be a valid configuration file in .yml"""

        filePath = f"configurations/commands/{name}.yml"
        result = None

        with open(file=filePath) as f:
            yamlFile = yaml.safe_load(f)
            result = yamlFile

        return result
