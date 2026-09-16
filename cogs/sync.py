"""Discord command syncing"""

import logging
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from bot import PatreonMemberRolesBot


class Sync(commands.Cog):
    """Syncs the slashcommands to discord"""

    def __init__(self, bot: PatreonMemberRolesBot):
        self.bot = bot
        self.logger = logging.getLogger("sync")

    @app_commands.command(name="sync", description="Sync commands")
    @app_commands.describe(guilds="Guilds to sync", spec="Type of sync")
    async def sync(
        self,
        interaction: discord.Interaction,
        guilds: str | None = None,
        spec: Literal["~", "*", "^"] | None = None,
    ) -> None:
        """Main sync command"""
        is_owner = await self.bot.is_owner(interaction.user)
        if is_owner:
            await interaction.response.defer()
            if not guilds:
                if spec == "~":
                    synced = await self.bot.tree.sync(guild=interaction.guild)
                elif spec == "*":
                    if interaction.guild is not None:
                        self.bot.tree.copy_global_to(guild=interaction.guild)
                    synced = await self.bot.tree.sync(guild=interaction.guild)
                elif spec == "^":
                    self.bot.tree.clear_commands(guild=interaction.guild)
                    await self.bot.tree.sync(guild=interaction.guild)
                    synced = []
                else:
                    synced = await self.bot.tree.sync()
                items = [item.name for item in synced]
                sync_type_msg = "globally" if spec is None else "to the current guild."
                await interaction.followup.send(
                    f"Synced {len(synced)} commands {sync_type_msg}"
                )
                self.logger.info("synced commands:")
                self.logger.info(items)
                return

            ret = 0
            for guild in guilds.split(" "):
                try:
                    await self.bot.tree.sync(guild=discord.Object(id=guild))
                except discord.HTTPException:
                    pass
                else:
                    ret += 1

            await interaction.followup.send(
                f"Synced the tree to {ret}/{len(guilds.split(' '))}."
            )

    @sync.error
    async def bfsync_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        """On command error"""
        self.logger.error(error)
        await interaction.followup.send(f"Failed to sync:\n{error}")


async def setup(bot: PatreonMemberRolesBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(Sync(bot), guild=discord.Object(770746735533228083))
