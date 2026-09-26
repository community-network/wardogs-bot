"""User management"""

import logging

import discord
from discord import app_commands
from discord.ext import commands

from bot import WardogsBot
from constants import stat_items
from database.functions import discord_role_groups, discord_roles


class Admin(commands.Cog):
    def __init__(self, bot: WardogsBot):
        self.bot = bot
        self.logger = logging.getLogger("admin")

    group = app_commands.Group(
        name="admin", description="Commands meant only for admins"
    )

    roles = app_commands.Group(name="roles", description="Roles commands", parent=group)

    async def generate_roles_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        """Autocomplete role groups"""
        async with self.bot.db.create_session() as session:
            if interaction.guild is None:
                return []
            role_groups = await discord_role_groups.get_all(
                session, interaction.guild.id
            )
            return [
                app_commands.Choice(name=role_group.name, value=role_group.name)
                for role_group in role_groups
                if role_group.name.lower().startswith(current.lower())
            ][:25]

    @roles.command(
        name="generate",
        description="Generate roles by group",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        stats_item=[
            app_commands.Choice(name=stat_item, value=stat_item)
            for stat_item in stat_items.stat_items
        ]
    )
    @app_commands.describe(
        step="Steps between the roles",
        min_role="smallest role to generate",
        max_role="maximum role to generate",
    )
    async def generate_roles(
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
            existing_role = await discord_role_groups.get_by_name(
                session, interaction.guild.id, stats_item.value
            )
            if existing_role is not None:
                await interaction.followup.send(
                    "Role group already exists", ephemeral=True
                )

            role_group = await discord_role_groups.create(
                session, interaction.guild.id, stats_item.value
            )
            for index in range(min_role, max_role, step):
                role_name = f"{stats_item.value} {index}-{index + step}"

                role = await interaction.guild.create_role(name=role_name)
                await discord_roles.create(
                    session,
                    role.id,
                    role_group.id,
                    role_name,
                    stats_item.value,
                    index,
                    index + step,
                )

        await interaction.followup.send("Created the roles", ephemeral=True)

    sync = app_commands.Group(name="sync", description="Sync commands", parent=group)

    @roles.command(
        name="remove",
        description="Remove the roles by group",
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.autocomplete(stats_item=generate_roles_autocomplete)
    async def remove_roles_by_group(
        self, interaction: discord.Interaction, stats_item: str
    ) -> None:
        await interaction.response.defer()
        if interaction.guild is None:
            return  # is already set to guild_only
        async with self.bot.db.create_session() as session:
            try:
                role_group = await discord_role_groups.get_by_name(
                    session, interaction.guild.id, stats_item
                )
                if role_group is None:
                    await interaction.response.send_message(
                        "Role does not exist", ephemeral=True
                    )
                    return

                for db_role in await role_group.awaitable_attrs.discord_roles:
                    role = interaction.guild.get_role(db_role.id)
                    if role is not None:
                        await role.delete()
                    await discord_roles.remove(session, db_role.id)
                await discord_role_groups.remove(session, role_group.id)
                await interaction.followup.send(
                    "Removed the role group", ephemeral=True
                )
            except Exception as e:
                print(e)


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Admin(bot))
