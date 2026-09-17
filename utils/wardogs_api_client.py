import discord
from kiota_abstractions.authentication import AnonymousAuthenticationProvider
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

from client.wardogs_api import WardogsApi
from config import Config


def create_wardogs_client(config: Config):
    auth_provider = AnonymousAuthenticationProvider()
    request_adapter = HttpxRequestAdapter(auth_provider)
    request_adapter.base_url = config.bot.auth_base_url
    client = WardogsApi(request_adapter)
    return client


async def create_stats_embed(config: Config, user_id: int):
    client = create_wardogs_client(config)
    stats = await client.stats.get(
        request_configuration=RequestConfiguration(
            query_parameters=client.stats.StatsRequestBuilderGetQueryParameters(
                discord_id=user_id
            )
        )
    )

    if stats is None:
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

    embed.set_footer(text=(f"PlayerData version: {stats.player_data_version.integer}"))
    return embed
