import discord

from utils.buttons import RefreshButton


class RefreshStatsView(discord.ui.View):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(
            RefreshButton(
                self.bot,
                label="Refresh stats",
                custom_id="refresh_stats",
            )
        )
