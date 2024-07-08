from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_user(self, telegram_id: int, group_id: int):
        session = self.session
        query = select(User).where(User.telegram_id == telegram_id)
        user = await session.execute(query)
        user = user.scalar()
        if user is not None:
            await session.execute(
                update(User)
                .where(User.telegram_id == telegram_id)
                .values(group_id=group_id)
            )
        else:
            await session.execute(
                insert(User).values(telegram_id=telegram_id, group_id=group_id)
            )

        await session.commit()
