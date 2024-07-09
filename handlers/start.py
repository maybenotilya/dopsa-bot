from aiogram import Router, types
from aiogram.filters import Command

from consts import commands, Messages

router = Router()


@router.message(Command(commands["start"]))
async def start(message: types.Message):
    await message.answer(Messages.start_message)


@router.message(Command(commands["help"]))
async def help(message: types.Message):
    await message.answer(Messages.help_message)
