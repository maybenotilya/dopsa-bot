from aiogram import F, Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from consts import commands, Messages

router = Router()


@router.message(Command(commands["start"]))
async def start(message: types.Message):
    await message.answer(Messages.start_message)


@router.message(Command(commands["help"]))
async def help(message: types.Message):
    await message.answer(Messages.help_message)
