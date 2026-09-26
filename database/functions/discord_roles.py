from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.dto import DiscordRole


async def get(
    session: AsyncSession,
    id: int,
) -> DiscordRole | None:
    stmt = select(DiscordRole).filter(DiscordRole.id == id).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[DiscordRole]:
    stmt = select(DiscordRole)
    result = await session.execute(stmt)
    return [item for item in result.scalars().all()]


async def create(
    session: AsyncSession,
    id: int,
    role_group_id: int,
    name: str,
    tracked_item: str,
    role_range_min: int,
    role_range_max: int,
) -> DiscordRole:
    channel = {
        "id": id,
        "name": name,
        "discord_role_group_id": role_group_id,
        "tracked_item": tracked_item,
        "role_range_min": role_range_min,
        "role_range_max": role_range_max,
    }
    stmt = insert(DiscordRole).values(channel).returning(DiscordRole)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one()


async def remove(session: AsyncSession, role_id: int):
    voice_channel = await get(session, role_id)
    await session.delete(voice_channel)
    await session.commit()
