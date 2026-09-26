import asyncio
import logging
import os

import discord
from discord.ext import commands
from fastapi import FastAPI, Query
from fastapi.concurrency import asynccontextmanager

from config import load_config
from database.connection import DatabaseSingleton
from logger import setup_logger
from utils.create_update_url import _consume_pending_state, _get_pending_state
from utils.sync_roles import sync_roles
from utils.wardogs_api_client import create_stats_embed, get_stats

env_config = load_config()

logger = logging.getLogger("bot")
setup_logger(logger)


class WardogsBot(commands.AutoShardedBot):
    """Bot setup class."""

    def __init__(self, *args, **kwargs):
        self.logger = logger
        self.config = env_config
        self.db = DatabaseSingleton(env_config.db)
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.db.init_db()
        self.remove_command("help")
        await self.load_cogs()
        logger.info("Bot started")

    async def load_cogs(self):
        for file in os.listdir(os.path.dirname(os.path.abspath(__file__)) + "/cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                await bot.load_extension(f"cogs.{name}")
                self.logger.info(f"Loaded cog: {name}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(bot.start(env_config.bot.discord_bot_token))
    yield
    await bot.close()
    await bot.db.close_async()


intents = discord.Intents.default()
intents.members = True
bot = WardogsBot(command_prefix="!", intents=intents)
app = FastAPI(lifespan=lifespan)


@bot.event
async def on_ready():
    """After bot is logged into discord"""
    await bot.tree.sync()


@bot.event
async def on_command_error(ctx, error):
    """dont give a error if a command doesn't exist"""
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            color=0xE74C3C, description="Your not allowed to use this command"
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.NoPrivateMessage):
        embed = discord.Embed(
            color=0xE74C3C,
            description="This command can only be used within a community, not in DM",
        )
        await ctx.send(embed=embed)
    else:
        raise error


@app.post("/notify")
async def notify(
    state_id: str = Query(
        "",
        description="Channel id",
    ),
):
    state = _get_pending_state(state_id)
    if state is None:
        return {"error": "State invalid"}

    channel = bot.get_channel(state.get("channel_id", ""))
    if channel is None:
        return {"error": "Channel not found"}

    try:
        if (
            isinstance(channel, discord.abc.GuildChannel)
            and not isinstance(channel, discord.CategoryChannel)
            and not isinstance(channel, discord.ForumChannel)
        ):
            stats = await get_stats(bot.config, state.get("discord_id", ""))
            if stats is not None:
                embed = create_stats_embed(stats)
                await channel.send(
                    content=f"<@{state.get('discord_id', '')}>", embed=embed
                )
                await sync_roles(bot, state, stats)
            else:
                await channel.send(
                    content=f"<@{state.get('discord_id', '')}> Your WARDOGS account is linked, but no stat snapshot has been saved yet.",
                )

            message = await channel.fetch_message(state.get("message_id", ""))
            if message is not None:
                await channel.delete_messages([message])

        _consume_pending_state(state_id)
    except Exception as e:
        print(e)

    return {"ok": True}
