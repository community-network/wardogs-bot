import asyncio
import logging
import os

import discord
from discord.ext import commands

from config import load_config
from database.connection import DatabaseSingleton
from logger import setup_logger

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


intents = discord.Intents.default()
intents.members = True
bot = WardogsBot(command_prefix="!", intents=intents)


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


async def main() -> None:
    async with bot:
        await bot.start(env_config.bot.discord_bot_token)


if __name__ == "__main__":
    asyncio.run(main())
