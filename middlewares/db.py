from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from db.manager import DatabaseManager


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session: async_sessionmaker):
        super().__init__()
        self.session = session

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session() as session:
            db_manager = DatabaseManager(session)
            data["db_manager"] = db_manager
            return await handler(event, data)
