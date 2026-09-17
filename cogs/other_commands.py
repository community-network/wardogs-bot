"""Non-grouped commands"""

import discord
from discord import app_commands
from discord.ext import commands

from bot import WardogsBot


class OtherCommands(commands.Cog):
    """Other commands"""

    def __init__(self, bot: WardogsBot):
        self.bot = bot

    @app_commands.command(name="help", description="See more info about the bot")
    async def help_command(self, interaction: discord.Interaction):
        """Main help command"""
        await interaction.response.defer()
        embed = discord.Embed(
            color=0xFFA500,
            title="Help for the wardogs bot",
            description="This is a both where you can request stats from users with /stats",
        )
        await interaction.followup.send(embed=embed)


async def setup(bot: WardogsBot) -> None:
    """Setup the cog within discord.py lib"""
    await bot.add_cog(OtherCommands(bot))
