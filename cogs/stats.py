import logging
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from kiota_abstractions.api_error import APIError

from bot import WardogsBot
from utils.create_update_url import create_pending_state, create_update_url
from utils.wardogs_api_client import (
    create_stats_embed,
    get_stats,
)


class Stats(commands.Cog):
    """Stats commands"""

    def __init__(self, bot: WardogsBot):
        self.bot = bot
        self.logger = logging.getLogger("admin")

    async def start_update(self, interaction, description):
        login_url, id = create_update_url(
            self.bot.config.bot, interaction.user.id, interaction.user.display_name
        )
        view = discord.ui.View(timeout=600)
        view.add_item(
            discord.ui.Button(
                label="Sign in with Steam",
                url=login_url,
            )
        )
        embed = discord.Embed(title="Update WARDOGS Stats", description=description)

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )
        create_pending_state(id, interaction)

    @app_commands.command(
        name="update", description="Sign in with Steam and update your WARDOGS stats."
    )
    async def update_command(self, interaction: discord.Interaction):
        await self.start_update(
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
                await interaction.followup.send(embed=embed)
            elif member is not None:
                await interaction.followup.send(
                    "Your WARDOGS account is linked, but no stat snapshot has been saved yet.",
                    ephemeral=True,
                )
            else:
                await self.start_update(
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
                await self.start_update(
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
