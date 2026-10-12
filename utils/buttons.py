import discord

from cogs.functions.start_update import start_update


class RefreshButton(discord.ui.Button):
    def __init__(self, bot, label: str, custom_id: str):
        self.bot = bot
        super().__init__(
            style=discord.ButtonStyle.gray, label=label, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        # custom_id = interaction.data["custom_id"]
        await start_update(
            self.bot,
            interaction,
            (
                "Click **Sign in with Steam** below.\n\n"
                "After Steam authenticates your account, "
                "your current WARDOGS stats will be "
                "retrieved and saved.\n\n"
                "This login link expires after 10 minutes "
                "and can only be used once."
            ),
        )
