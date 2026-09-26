from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.dto import DiscordRoleGroup


async def get(
    session: AsyncSession,
    id: int,
) -> DiscordRoleGroup | None:
    stmt = select(DiscordRoleGroup).filter(DiscordRoleGroup.id == id).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_by_name(
    session: AsyncSession,
    name: str,
) -> DiscordRoleGroup | None:
    stmt = select(DiscordRoleGroup).filter(DiscordRoleGroup.name == name).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession) -> list[DiscordRoleGroup]:
    stmt = select(DiscordRoleGroup)
    result = await session.execute(stmt)
    return [item for item in result.scalars().all()]


async def create(
    session: AsyncSession,
    name: str,
) -> DiscordRoleGroup:
    channel = {
        "name": name,
    }
    stmt = insert(DiscordRoleGroup).values(channel).returning(DiscordRoleGroup)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one()


async def remove(session: AsyncSession, role_id: int):
    voice_channel = await get(session, role_id)
    await session.delete(voice_channel)
    await session.commit()
