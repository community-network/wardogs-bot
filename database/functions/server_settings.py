from typing import Optional

import discord
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.dto import ServerSetting


async def add_guild(session: AsyncSession, guild: discord.Guild, changes: dict) -> None:
    data = dict(server_id=guild.id, server_name=guild.name)
    data.update(changes)
    stmt = insert(ServerSetting).values(data)
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=[ServerSetting.server_id],
        set_=dict((k, v) for (k, v) in data.items() if k != "created_at"),
    )

    try:
        await session.execute(do_update_stmt)
        await session.commit()
    except IntegrityError:
        pass


async def update_guild(session: AsyncSession, guild: discord.Guild, changes: dict):
    if not await has_guild(session, guild.id):
        await add_guild(session, guild, changes)
        return

    stmt = (
        update(ServerSetting).where(ServerSetting.server_id == guild.id).values(changes)
    )
    await session.execute(stmt)
    await session.commit()


async def get_guild(session: AsyncSession, server_id: int) -> Optional[ServerSetting]:
    stmt = select(ServerSetting).filter(ServerSetting.server_id == server_id).limit(1)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def has_guild(session: AsyncSession, server_id: int) -> bool | None:
    exists_criteria = (
        select(ServerSetting.server_id)
        .filter(ServerSetting.server_id == server_id)
        .exists()
    )
    stmt = select(exists_criteria)
    return await session.scalar(stmt)
