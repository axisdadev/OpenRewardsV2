import nextcord
from nextcord import Embed


class Embeds():
    sucessEmbed = Embed(
        description="✅ Sucessfully completed action.",
        color=nextcord.Color(
            int("339900", 16),
        ),
    )

    warningEmbed = Embed(
        description="⚠️ Warning message",
        color=nextcord.Color(
            int("ffcc00", 16),
        ),
    )

    errorEmbed = Embed(
        description="❌ Oops! An error occured. Pardon our dust :)",
        color=nextcord.Color(
            int("cc3300", 16),
        ),
    )

    invalidPermissionEmbed = Embed(
        description="❌ You do not have the correct permissions to run this command.",
        color=nextcord.Color(
            int("cc3300", 16),
        ),
    )
