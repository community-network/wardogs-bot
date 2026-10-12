import logging
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from kiota_abstractions.api_error import APIError

from bot import WardogsBot
from cogs.functions.start_update import start_update
from utils.buttons import RefreshButton
from utils.wardogs_api_client import (
    create_stats_embed,
    get_stats,
)


class Stats(commands.Cog):
    """Stats commands"""

    def __init__(self, bot: WardogsBot):
        self.bot = bot
        self.logger = logging.getLogger("admin")

    @app_commands.command(
        name="update", description="Sign in with Steam and update your WARDOGS stats."
    )
    async def update_command(self, interaction: discord.Interaction):
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

    @app_commands.command(
        name="stats",
        description="Show your stats WARDOGS stats.",
    )
    async def stats(
        self, interaction: discord.Interaction, member: discord.Member | None = None
    ):
        await interaction.response.defer()
        user = member or interaction.user
        try:
            stats = await get_stats(self.bot.config, user.id)
            if stats is not None:
                embed = create_stats_embed(stats)
                view = discord.ui.View(timeout=600)
                view.add_item(
                    RefreshButton(
                        self.bot,
                        label="Refresh stats",
                        custom_id="refresh_stats",
                    )
                )
                await interaction.followup.send(embed=embed, view=view)
            elif member is not None:
                await interaction.followup.send(
                    "Your WARDOGS account is linked, but no stat snapshot has been saved yet.",
                    ephemeral=True,
                )
            else:
                await start_update(
                    self.bot,
                    interaction,
                    (
                        "Your WARDOGS account is linked, but no stat snapshot has been saved yet."
                        "Please try to update your stats\n\n"
                        "Click **Sign in with Steam** below.\n\n"
                        "After Steam authenticates your account, "
                        "your current WARDOGS stats will be "
                        "retrieved and saved.\n\n"
                        "This login link expires after 10 minutes "
                        "and can only be used once."
                    ),
                )

        except APIError as exc:
            if member is not None:
                await interaction.followup.send(
                    "Could not get any stats for the requested user.",
                    ephemeral=True,
                )
            else:
                await start_update(
                    self.bot,
                    interaction,
                    (
                        "Could not get any stats for the requested user."
                        "Please try to update your stats\n\n"
                        "Click **Sign in with Steam** below.\n\n"
                        "After Steam authenticates your account, "
                        "your current WARDOGS stats will be "
                        "retrieved and saved.\n\n"
                        "This login link expires after 10 minutes "
                        "and can only be used once."
                    ),
                )
            if exc.response_status_code != 404:
                self.logger.error(
                    f"Could not get stats for user {interaction.user.name}: {type(exc).__name__}: {exc}",
                    traceback.format_exc(),
                )


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Stats(bot))
