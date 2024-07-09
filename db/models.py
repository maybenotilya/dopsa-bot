import os

from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True)
    group_id = Column(Integer)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger, unique=True)
    group_name = Column(String, unique=True)


async def async_main(engine: AsyncEngine):
    if (
        not os.path.exists(os.environ["DOPSABOT_JSON_DB_PATH"])
        or os.environ["DOPSABOT_DROP_ON_RESTART"]
    ):
        with open(os.environ["DOPSABOT_JSON_DB_PATH"], "w") as f:
            f.write("{}")
    async with engine.begin() as conn:
        if os.environ["DOPSABOT_DROP_ON_RESTART"]:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
