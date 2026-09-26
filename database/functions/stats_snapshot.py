from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dto import DiscordUser, StatsSnapshot, WardogAccount
from database.functions import unlocks
from dto.wardogs_models import PlayerStats, RoleStats


async def get_latest(
    session: AsyncSession,
    account_id: int | None,
    steam_id: int | None,
    discord_id: int | None,
) -> PlayerStats | None:
    stmt = select(StatsSnapshot)
    if account_id is not None:
        stmt = stmt.filter(StatsSnapshot.account_id == account_id)
    elif steam_id is not None:
        stmt = stmt.filter(WardogAccount.steam_id == str(steam_id))
    elif discord_id is not None:
        stmt = stmt.filter(DiscordUser.discord_id == discord_id)
    stmt = stmt.order_by(StatsSnapshot.id.desc()).limit(1)
    result = await session.execute(stmt)
    res = result.scalar_one_or_none()
    if res is None:
        return None

    cur_unlocks = await unlocks.get(session, res.account_id)

    return PlayerStats(
        player_data_version=res.player_data_version,
        infantry=RoleStats(res.infantry_level, res.infantry_xp),
        medic=RoleStats(res.medic_level, res.medic_xp),
        recon=RoleStats(res.recon_level, res.recon_xp),
        support=RoleStats(res.support_level, res.support_xp),
        driver=RoleStats(res.driver_level, res.driver_xp),
        pilot=RoleStats(res.pilot_level, res.pilot_xp),
        cash=res.cash,
        gold=res.gold,
        unlocks=cur_unlocks,
    )
