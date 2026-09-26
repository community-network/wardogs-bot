from discord.ext import commands

from client.models.player_stats import PlayerStats
from database.functions import discord_roles


async def sync_roles(bot: commands.AutoShardedBot, state: dict, stats: PlayerStats):
    guild = bot.get_guild(state.get("server_id", 0))
    if guild is None:
        return

    async with bot.db.create_session() as session:
        roles = await discord_roles.get_all(session)
        for role in roles:
            discord_role = guild.get_role(role.id)
            if discord_role is None:
                print("missing role!")
                pass
