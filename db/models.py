from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger)
    group_id = Column(Integer)


async def async_main(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
