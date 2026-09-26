from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.dto import Unlock
from dto.wardogs_models import UnlockInfo


async def get(session: AsyncSession, account_id: int) -> list[UnlockInfo]:
    stmt = select(Unlock).filter(Unlock.account_id == account_id)
    res = (await session.execute(stmt)).scalars().all()
    return [UnlockInfo(str(item.node_id), item.level) for item in res]
