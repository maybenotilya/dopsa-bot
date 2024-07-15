import os
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

import asyncio
import logging
from aiogram import Dispatcher, Bot
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import start, register
from db.models import async_main
from middlewares.db import DbSessionMiddleware
from middlewares.bot import BotMiddleware
from notifier.notifier import scheduled_notify


logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["DOPSABOT_API_TOKEN"])
dp = Dispatcher()


async def main():
    engine = create_async_engine(url=os.environ["DOPSABOT_SQLITE_URL"], echo=True)
    await async_main(engine)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp.update.middleware(DbSessionMiddleware(session=sessionmaker))
    dp.update.middleware(BotMiddleware(bot))
    dp.include_routers(start.router, register.router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        scheduled_notify,
        trigger="interval",
        seconds=60 * 30,
        kwargs={"bot": bot, "session": sessionmaker},
    )
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
