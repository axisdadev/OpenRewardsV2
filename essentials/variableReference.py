from nextcord import Interaction
from essentials.logger import setup_logger
from essentials import database
import re

# Predefined references (with placeholders)
variable_references = {
    "user": {
        "name": "Interaction.user.name",
        "id": "Interaction.user.id",
        "display": "Interaction.user.display_name",
        "nickname": "Interaction.user.nick",
        "mention": "Interaction.user.mention",
        "avatar": "Interaction.user.avatar.url",
        "banner": "Interaction.user.banner.url",
        "points": """$["points"]""",
        "items": """$["itemsOwned"]""",
    },
}


async def get_reference(variable: str, interaction: Interaction, ignoreWarning: bool):
    """
    Get a reference and return the value
    
    :param variable: The variable to search for in the refrences list.
    :param interaction: Nextcord interaction, must be used within a command.
    :param ignoreWarning: When using custom variables, the references system is programmed to output if a certain refernce isn't found.
    :returns: str, True if the refrence is found correctly and translated properly.
    """
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
                if ignoreWarning:
                    return None, False
                else:
                    logger.warning(f"Error accessing {item}: {e}")
                    return None, False
        else:
            if ignoreWarning:
                return None, False
            else:
                logger.warning(f"Item '{item}' not found in category '{category}'.")
                return None, False
    else:
        if ignoreWarning:
            return None, False
        else:
            logger.warning(f"Category '{category}' not found.")
            return None, False


async def replace_references(
    string: str, interaction: Interaction, customReferences: dict
):
    """
    Replaces all of the refrences in a string.

    :param string: The string that is altered with the correct refrences.
    :param interaction: The nextcord interaction type, required to be used within an async command
    :param customReferences: If wanted, use custom variables passed down with data.

    :returns: str
    """
    pattern = r"\{(.*?)\}"
    matches = re.findall(pattern=pattern, string=string)
    logger = setup_logger()

    for match in matches:
        # Try to get the reference using the existing get_reference function
        replaceRefrence, success = await get_reference(match, interaction, True)

        if not success:
            try:
                # Try to get the value from customRefrences if not found in standard references
                if match in customReferences:
                    value = customReferences[match]
                    string = string.replace(
                        f"{{{match}}}", str(value)
                    )  # Replace in the string
                else:
                    logger.warning(f"Custom reference '{match}' not found.")
            except Exception as e:
                logger.error(f"Error while accessing custom reference '{match}': {e}")
        else:
            # Replace in the string using the value from get_reference
            string = string.replace(f"{{{match}}}", str(replaceRefrence))

    return string
