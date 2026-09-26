import logging

import discord
from discord import app_commands
from discord.ext import commands

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

    @app_commands.command(
        name="update", description="Sign in with Steam and update your WARDOGS stats."
    )
    async def update_command(self, interaction: discord.Interaction):
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

        msg = await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True,
        )
        create_pending_state(id, interaction, msg.id)

    @app_commands.command(
        name="stats",
        description="Show your stats WARDOGS stats.",
    )
    async def stats(
        self, interaction: discord.Interaction, member: discord.Member | None = None
    ):
        await interaction.response.defer()
        user = member or interaction.user
        stats = await get_stats(self.bot.config, user.id)
        if stats is not None:
            embed = create_stats_embed(stats)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                "Your WARDOGS account is linked, but no stat snapshot has been saved yet.",
                ephemeral=True,
            )


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Stats(bot))
