import os
import pickle
import aiofiles

from typing import List, Dict
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User, Group
from views import GroupView, UserView, ExamView, map_group, map_user


class DatabaseManager:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_groups(self) -> List[GroupView]:
        session = self.session
        query = select(Group).options(selectinload(Group.users))
        groups = (await session.execute(query)).scalars().all()
        return [map_group(group) for group in groups]

    async def get_users(self) -> List[UserView]:
        session = self.session
        query = select(User).options(joinedload(User.group))
        users = (await session.execute(query)).unique().scalars().all()
        return [map_user(user) for user in users]

    async def get_user_by_telegram_id(self, telegram_id: int) -> UserView:
        session = self.session
        query = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(query)).scalar_one_or_none()
        return None if user is None else map_user(user)

    async def get_exams(self) -> Dict[int, List[ExamView]]:
        async with aiofiles.open(os.environ["DOPSABOT_EXAMS_DB_PATH"], "rb") as db:
            return pickle.loads(await db.read())

    async def insert_group(self, group_id: int, group_name: str):
        session = self.session
        query = select(Group).where(Group.group_id == group_id)
        group = (await session.execute(query)).scalar_one_or_none()

        if group is None:
            group = Group(group_id=group_id, group_name=group_name)
            session.add(group)

        session.commit()

    async def upsert_user(self, telegram_id: int, group_id: int, group_name: str):
        session = self.session
        group_query = select(Group).where(Group.group_id == group_id)
        group = (await session.execute(group_query)).scalar_one_or_none()

        if group is None:
            group = Group(group_id=group_id, group_name=group_name)
            session.add(group)

        user_query = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(user_query)).scalar_one_or_none()

        if user is None:
            user = User(telegram_id=telegram_id, group_id=group_id, group=group)
            session.add(user)
        else:
            user.group = group

        await session.commit()

    async def dumb_exams(self, exams: Dict[int, List[ExamView]]):
        async with aiofiles.open(os.environ["DOPSABOT_EXAMS_DB_PATH"], "wb") as db:
            await db.write(pickle.dumps(exams))

    async def get_number_groups(self):
        session = self.session
        query = select(func.count()).select_from(Group)
        return (await session.execute(query)).scalar()
