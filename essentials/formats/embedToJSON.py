import json
import nextcord

def json_to_nextcord_embed(json_string):
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

# Example JSON string for testing
json_string = '''
{
    "title": "This is a test embed",
    "description": "Description of the embed",
    "color": 15158332,
    "fields": [
        {"name": "Field 1", "value": "This is field 1", "inline": true},
        {"name": "Field 2", "value": "This is field 2", "inline": false}
    ],
    "footer": {"text": "Footer text", "icon_url": "https://example.com/footer.png"},
    "thumbnail": {"url": "https://example.com/thumbnail.png"},
    "author": {"name": "Author Name", "icon_url": "https://example.com/author.png"}
}
'''

# Convert the JSON to a nextcord embed
embed = json_to_nextcord_embed(json_string)

# Now you can send the embed using a bot, for example in an on_message event
# await message.channel.send(embed=embed)
