import discord

from bot import WardogsBot
from utils.create_update_url import create_pending_state, create_update_url


async def start_update(
    bot: WardogsBot, interaction: discord.Interaction, description: str
):
    login_url, id = create_update_url(
        bot.config.bot, interaction.user.id, interaction.user.display_name
    )
    view = discord.ui.View(timeout=600)
    view.add_item(
        discord.ui.Button(
            label="Sign in with Steam",
            url=login_url,
        )
    )
    embed = discord.Embed(title="Update WARDOGS Stats", description=description)

    await interaction.followup.send(
        embed=embed,
        view=view,
        ephemeral=True,
    )
    create_pending_state(id, interaction)
