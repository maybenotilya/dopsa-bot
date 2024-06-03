import asyncio
import logging
import os
from aiogram import Dispatcher, Bot
from handlers import start, register

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=os.environ["DOPSABOT_API_TOKEN"])
    dp = Dispatcher()
    dp.include_routers(start.router, register.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
