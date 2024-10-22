import json
import nextcord
import re

def jsonToEmbed(json_string):
    # Parse the JSON string into a Python dictionary
    embed_data = json.loads(json_string)

    # Create the embed object
    embed = nextcord.Embed(
        title=embed_data.get("title", ""),
        description=embed_data.get("description", ""),
        color=nextcord.Color(embed_data.get("color", 0))  # default color is 0 (no color)
    )

    # Add additional fields if present
    if "url" in embed_data:
        embed.url = embed_data["url"]
    if "timestamp" in embed_data:
        embed.timestamp = embed_data["timestamp"]
    if "footer" in embed_data:
        embed.set_footer(text=embed_data["footer"].get("text", ""), icon_url=embed_data["footer"].get("icon_url", ""))
    if "image" in embed_data:
        embed.set_image(url=embed_data["image"].get("url", ""))
    if "thumbnail" in embed_data:
        embed.set_thumbnail(url=embed_data["thumbnail"].get("url", ""))
    if "author" in embed_data:
        embed.set_author(name=embed_data["author"].get("name", ""), url=embed_data["author"].get("url", ""), icon_url=embed_data["author"].get("icon_url", ""))
    if "fields" in embed_data:
        for field in embed_data["fields"]:
            embed.add_field(name=field.get("name", ""), value=field.get("value", ""), inline=field.get("inline", True))

    return embed

def extractVariables(obj):
    results = []

    # Regular expression to find text inside {}
    pattern = re.compile(r'\{([^}]*)\}')

    if isinstance(obj, dict):
        for key, value in obj.items():
            # Check key and value for the pattern
            if isinstance(key, str):
                results += pattern.findall(key)
            if isinstance(value, str):
                results += pattern.findall(value)
            else:
                # Recursive call if the value is a dict or list
                results += extractVariables(value)

    elif isinstance(obj, list):
        for item in obj:
            results += extractVariables(item)

    return results

def replaceVariables(obj, replacement_text):
    pattern = re.compile(r'\{([^}]*)\}')

    if isinstance(obj, dict):
        for key, value in list(obj.items()):
            # Replace text in keys
            if isinstance(key, str):
                new_key = pattern.sub(replacement_text, key)
                if new_key != key:
                    obj[new_key] = obj.pop(key)
                key = new_key
            # Replace text in values
            if isinstance(value, str):
                obj[key] = pattern.sub(replacement_text, value)
            else:
                # Recursive call for dicts or lists
                replaceVariables(value, replacement_text)

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, str):
                obj[i] = pattern.sub(replacement_text, item)
            else:
                replaceVariables(item, replacement_text)