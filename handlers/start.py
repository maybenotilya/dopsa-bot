from aiogram import Router, types
from aiogram.filters import Command

from consts import BotCommands, Messages
from db.manager import DatabaseManager
from formatters import format_exams

router = Router()


@router.message(Command(BotCommands.start))
async def start(message: types.Message):
    await message.answer(Messages.start_message)


@router.message(Command(BotCommands.help))
async def help(message: types.Message):
    await message.answer(Messages.help_message)


@router.message(Command(BotCommands.rasp))
async def rasp(message: types.Message, db_manager: DatabaseManager):
    user = await db_manager.get_user_by_telegram_id(message.from_user.id)
    if user is None:
        await message.answer(Messages.no_register_message)
        return

    exams = (await db_manager.get_exams()).get(user.group_id, [])

    if len(exams) == 0:
        await message.answer(Messages.no_exams_message)
        return

    message_text = Messages.month_exams_message + format_exams(exams)
    await message.answer(message_text)
