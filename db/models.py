import os
import pickle
import aiofiles

from typing import List

from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped
from sqlalchemy.ext.asyncio import AsyncEngine


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[BigInteger] = Column(BigInteger, unique=True)
    group_id: Mapped[int] = Column(Integer, ForeignKey("groups.group_id"))
    group: Mapped["Group"] = relationship("Group", back_populates="users")


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    group_id: Mapped[int] = Column(Integer, unique=True)
    group_name: Mapped[str] = Column(String, unique=True)
    users: Mapped[List["User"]] = relationship("User", back_populates="group")


async def async_main(engine: AsyncEngine):
    if int(os.environ["DOPSABOT_DROP_ON_RESTART"]) or not os.path.exists(
        os.environ["DOPSABOT_DROP_ON_RESTART"]
    ):
        async with aiofiles.open(os.environ["DOPSABOT_EXAMS_DB_PATH"], "wb") as db:
            await db.write(pickle.dumps({}))

    async with engine.begin() as conn:
        if int(os.environ["DOPSABOT_DROP_ON_RESTART"]):
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
