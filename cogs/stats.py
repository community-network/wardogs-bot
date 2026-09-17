import logging

import discord
from discord import app_commands
from discord.ext import commands

from bot import WardogsBot
from utils.create_update_url import create_update_url


class Stats(commands.Cog):
    def __init__(self, bot: WardogsBot):
        self.bot = bot
        self.logger = logging.getLogger("admin")

    @app_commands.command(
        name="update", description="Sign in with Steam and update your WARDOGS stats."
    )
    async def update(self, interaction: discord.Interaction):
        login_url = create_update_url(self.bot.config.bot, str(interaction.user.id))
        view = discord.ui.View(timeout=600)
        view.add_item(
            discord.ui.Button(
                label="Sign in with Steam",
                url=login_url,
            )
        )
        embed = discord.Embed(
            title="Update WARDOGS Stats",
            description=(
                "Click **Sign in with Steam** below.\n\n"
                "After Steam authenticates your account, "
                "your current WARDOGS stats will be "
                "retrieved and saved.\n\n"
                "This login link expires after 10 minutes "
                "and can only be used once."
            ),
        )

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Stats(bot))
