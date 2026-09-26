from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.dto import DiscordRoleGroup


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
