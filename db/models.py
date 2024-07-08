import os

from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True)
    group_id = Column(Integer)


async def async_main(engine: AsyncEngine):
    async with engine.begin() as conn:
        if os.environ["DOPSABOT_RECREATE_DB"]:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
