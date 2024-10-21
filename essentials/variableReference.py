from nextcord import Interaction
from essentials.logger import setup_logger
from essentials import database

# Predefined references (with placeholders)
variable_references = {
    "user": {
        "name": "Interaction.user.name",
        "id": "Interaction.user.id",
        "display": "Interaction.user.display_name",
        "nickname": "Interaction.user.nick",
        "avatar": "Interaction.user.avatar.url",
        "banner": "Interaction.user.banner.url",
        "points": """$["points"]""",
        "items": """$["itemsOwned"]""",
    },
}


async def get_reference(
    variable: str, interaction: Interaction, additionalParams: dict
):
    logger = setup_logger()
    split_name = variable.split(sep=".", maxsplit=1)

    databaseManager = database.DatabaseManager()

    if len(split_name) != 2:
        logger.warning(f"Referenced variable '{variable}' is invalid. Returning None.")
        return None, False

    category, item = split_name[0], split_name[1]

    if category in variable_references:
        category_data = variable_references[category]

        if item in category_data:
            try:
                if str(category_data[item]).startswith("$"):
                    try:
                        profile = await databaseManager.fetchProfile(
                            interaction.user.id
                        )
                        value = eval(category_data[item], {"$": profile})
                        return value, True
                    except Exception:
                        return None, False
                else:
                    value = eval(category_data[item], {"Interaction": interaction})
                    return value, True
            except AttributeError as e:
                logger.warning(f"Error accessing {item}: {e}")
                return None, False
        else:
            logger.warning(f"Item '{item}' not found in category '{category}'.")
            return None, False
    else:
        logger.warning(f"Category '{category}' not found.")
        return None, False
