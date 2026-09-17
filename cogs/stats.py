import logging

import discord
from discord import app_commands
from discord.ext import commands
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

from bot import WardogsBot
from client.wardogs_api import WardogsApi
from utils.create_update_url import create_pending_state, create_update_url


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
        create_pending_state(
            id, interaction.guild_id, interaction.channel_id, msg.message_id
        )

    @app_commands.command(
        name="stats",
        description="Show your stats WARDOGS stats.",
    )
    async def stats(self, interaction: discord.Interaction):
        auth_provider = AnonymousAuthenticationProvider()
        request_adapter = HttpxRequestAdapter(auth_provider)
        request_adapter.base_url = self.bot.config.bot.auth_base_url
        client = WardogsApi(request_adapter)
        stats = await client.stats.get(
            request_configuration=RequestConfiguration(
                query_parameters=client.stats.StatsRequestBuilderGetQueryParameters(
                    discord_id=interaction.user.id
                )
            )
        )

        if stats is None:
            await interaction.response.send_message(
                "Your WARDOGS account is linked, but "
                "no stat snapshot has been saved yet.",
                ephemeral=True,
            )

            return

        embed = discord.Embed(
            title="WARDOGS Player Stats",
            description=(f"**Wardog Level {stats.wardog_level}**"),
        )

        embed.add_field(
            name="Infantry",
            value=(f"Level **{stats.infantry.level}**\nXP: {stats.infantry.xp:,}"),
            inline=True,
        )

        embed.add_field(
            name="Medic",
            value=(f"Level **{stats.medic.level}**\nXP: {stats.medic.xp:,}"),
            inline=True,
        )

        embed.add_field(
            name="Recon",
            value=(f"Level **{stats.recon.level}**\nXP: {stats.recon.xp:,}"),
            inline=True,
        )

        embed.add_field(
            name="Support",
            value=(f"Level **{stats.support.level}**\nXP: {stats.support.xp:,}"),
            inline=True,
        )

        embed.add_field(
            name="Driver",
            value=(f"Level **{stats.driver.level}**\nXP: {stats.driver.xp:,}"),
            inline=True,
        )

        embed.add_field(
            name="Pilot",
            value=(f"Level **{stats.pilot.level}**\nXP: {stats.pilot.xp:,}"),
            inline=True,
        )

        embed.add_field(
            name="Cash",
            value=f"{stats.cash:,}",
            inline=True,
        )

        embed.add_field(
            name="Gold",
            value=f"{stats.gold:,}",
            inline=True,
        )

        embed.add_field(
            name="Unlocks",
            value=str(len(stats.unlocks)),
            inline=True,
        )

        embed.set_footer(
            text=(f"PlayerData version: {stats.player_data_version.integer}")
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Stats(bot))
