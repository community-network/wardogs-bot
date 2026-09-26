import logging
import traceback
from constants import stat_items
from discord.ext import commands

from client.models.player_stats import PlayerStats
from database.functions import discord_role_groups

logger = logging.getLogger("admin")


async def sync_roles(bot: commands.AutoShardedBot, state: dict, stats: PlayerStats):
    guild = bot.get_guild(state.get("server_id", 0))
    if guild is None:
        return

    member = guild.get_member(state.get("discord_id", 0))
    if member is None:
        return

    async with bot.db.create_session() as session:
        try:
            role_groups = await discord_role_groups.get_all(
                session, state.get("server_id", 0)
            )
            for role_group in role_groups:
                for db_role in await role_group.awaitable_attrs.discord_roles:
                    level: int | None = None
                    if role_group.name in stat_items.role_stat_items:
                        level = getattr(stats, role_group.name).level  # type: ignore
                    else:
                        level = getattr(stats, role_group.name)
                    if level is None:
                        continue

                    should_have_role = (
                        level >= db_role.role_range_min
                        and level < db_role.role_range_max
                    )
                    cur_role = member.get_role(db_role.id)

                    discord_role = guild.get_role(db_role.id)
                    if discord_role is None:
                        continue

                    if cur_role is None and should_have_role:
                        await member.add_roles(discord_role)
                    if cur_role is not None and not should_have_role:
                        await member.remove_roles(cur_role)
        except Exception as exc:
            logger.error(
                f"Role update failed: {type(exc).__name__}: {exc}",
                traceback.format_exc(),
            )
