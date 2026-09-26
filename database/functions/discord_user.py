from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dto import DiscordUser


async def get_all(session: AsyncSession) -> list[int] | None:
    stmt = select(DiscordUser.discord_id)
    result = await session.execute(stmt)
    return [item for item in result.scalars().all()]
