import json
import nextcord
import re
from essentials.logger import setup_logger

log = setup_logger()


def loadEmbedData(path):
    try:
        with open(path, mode="r") as data:
            response = json.load(fp=data)
            print(response)
            return response
    except Exception as e:
        log.warning(
            f"Unable to load embed data with path: {path} with exception being: {e}"
        )
        return None
    

def jsonToEmbed(jsonData: dict):
    embed_data = jsonData

    colorConverted = str(embed_data.get("color")).replace("#", "") # Had to make a special variable for this since getting the data and attempting to convert it doesnt work.

    # Create the embed object
    embed = nextcord.Embed(
        title=embed_data.get("title", ""),
        description=embed_data.get("description", ""),
        colour=nextcord.Color(
            int(colorConverted, 16)
        ),
    )

    if "url" in embed_data:
        embed.url = embed_data["url"]
    if "timestamp" in embed_data:
        embed.timestamp = embed_data["timestamp"]
    if "footer" in embed_data:
        embed.set_footer(
            text=embed_data["footer"].get("text", ""),
            icon_url=embed_data["footer"].get("icon_url", ""),
        )
    if "image" in embed_data:
        embed.set_image(url=embed_data["image"].get("url", ""))
    if "thumbnail" in embed_data:
        embed.set_thumbnail(url=embed_data["thumbnail"].get("url", ""))
    if "author" in embed_data:
        embed.set_author(
            name=embed_data["author"].get("name", ""),
            url=embed_data["author"].get("url", ""),
            icon_url=embed_data["author"].get("icon_url", ""),
        )
    if "fields" in embed_data:
        for field in embed_data["fields"]:
            embed.add_field(
                name=field.get("name", ""),
                value=field.get("value", ""),
                inline=field.get("inline", True),
            )

    return embed