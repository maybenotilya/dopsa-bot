from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Group
from db.views import UserView


class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users(self):
        session = self.session
        users = (await session.execute(select(User))).scalars().all()
        groups = (await session.execute(select(Group))).scalars().all()
        groups = {group.group_id: group.group_name for group in groups}
        return [
            UserView(
                telegram_id=user.telegram_id,
                group_id=user.group_id,
                group_name=groups[user.group_id],
            )
            for user in users
        ]

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

    async def insert_group(self, group_id: int, group_name: str):
        session = self.session
        query = select(Group).where(Group.group_id == group_id)
        group = await session.execute(query)
        group = group.scalar()
        if group is None:
            await session.execute(
                insert(Group).values(group_id=group_id, group_name=group_name)
            )
        await session.commit()
