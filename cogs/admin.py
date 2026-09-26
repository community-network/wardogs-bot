"""User management"""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from bot import WardogsBot
from database.functions import discord_role_groups, discord_roles


class Admin(commands.Cog):
    def __init__(self, bot: WardogsBot):
        self.bot = bot
        self.logger = logging.getLogger("admin")

    group = app_commands.Group(
        name="admin", description="Commands meant only for admins"
    )

    generate = app_commands.Group(
        name="generate", description="Generate commands", parent=group
    )

    @generate.command(
        name="roles",
        description="Generate the needed roles, or attach to the existing roles",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        stats_item=[
            app_commands.Choice(name="infantry", value="infantry"),
            app_commands.Choice(name="medic", value="medic"),
            app_commands.Choice(name="recon", value="recon"),
            app_commands.Choice(name="support", value="support"),
            app_commands.Choice(name="driver", value="driver"),
            app_commands.Choice(name="pilot", value="pilot"),
            app_commands.Choice(name="cash", value="cash"),
        ]
    )
    @app_commands.describe(
        step="Steps between the roles",
        min_role="smallest role to generate",
        max_role="maximum role to generate",
    )
    async def add_tracked_channel(
        self,
        interaction: discord.Interaction,
        stats_item: app_commands.Choice[str],
        step: int = 5,
        min_role: int = 0,
        max_role: int = 75,
    ) -> None:
        """Add a tracked channel"""
        await interaction.response.defer()
        if interaction.guild is None:
            return  # is already set to guild_only
        async with self.bot.db.create_session() as session:
            role_group = await discord_role_groups.create(session, stats_item.value)
            for index in range(min_role, max_role, step):
                role_name = f"{stats_item.value} {index}-{index + step}"
                existing_role = await discord_roles.get(session, role_name)
                if existing_role is not None:
                    pass

                role = await interaction.guild.create_role(name=role_name)
                await discord_roles.create(
                    session,
                    role.id,
                    role_group.id,
                    role_name,
                    stats_item.value,
                    min_role,
                    max_role,
                )

        await interaction.followup.send("Created the roles", ephemeral=True)

    sync = app_commands.Group(name="sync", description="Sync commands", parent=group)


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Admin(bot))
