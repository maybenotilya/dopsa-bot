import logging

from aiogram import F, Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from consts import commands, divisions_aliases
from db.models import User
from timetable_api import students_api


class Register(StatesGroup):
    choosing_division = State()
    choosing_level = State()
    choosing_year = State()
    choosing_program = State()
    choosing_group = State()


router = Router()


@router.message(StateFilter(None), Command(commands["exit"]))
async def exit(message: types.Message, state: FSMContext):
    await message.answer("Вы не регистрируетесь, отменять нечего.")


@router.message(Command(commands["exit"]))
async def exit(message: types.Message, state: FSMContext):
    await message.answer("Отменяю вашу регистрацию.")
    await state.clear()


@router.message(Command(commands["register"]))
async def register(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=k, callback_data=v)]
            for k, v in divisions_aliases.items()
        ]
    )
    await message.answer("Выберите название вашего факультета.", reply_markup=keyboard)
    await state.set_state(Register.choosing_division)


@router.callback_query(Register.choosing_division)
async def choosing_devision(callback: types.CallbackQuery, state: FSMContext):
    try:
        levels = students_api.get_study_levels(callback.data)
    except Exception as e:
        logging.error(e)
        await callback.message.answer(
            "Что-то пошло не так, попробуйте зарегистрироваться заново."
        )
        await state.clear()
        return
    await state.update_data(alias=callback.data, levels=levels)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=level, callback_data=str(i))]
            for i, level in enumerate(levels)
        ]
    )
    await callback.message.edit_text(
        "Выберите ваш уровень образования.", reply_markup=keyboard
    )
    await state.set_state(Register.choosing_level)


@router.callback_query(Register.choosing_level)
async def choosing_level(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        study_programs = students_api.get_study_level_programs(
            data["alias"], data["levels"][int(callback.data)]
        )
    except Exception as e:
        logging.error(e)
        await callback.message.answer(
            "Что-то пошло не так, попробуйте зарегистрироваться заново."
        )
        await state.clear()
        return
    await state.update_data(study_programs=study_programs)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=program.name, callback_data=str(i))]
            for i, program in enumerate(study_programs)
        ]
    )
    await callback.message.edit_text(
        "Выберите образовательную программу.", reply_markup=keyboard
    )
    await state.set_state(Register.choosing_program)


@router.callback_query(Register.choosing_program)
async def choosing_program(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        admission_years = students_api.get_admission_years(
            data["study_programs"], data["study_programs"][int(callback.data)].name
        )
    except Exception as e:
        logging.error(e)
        await callback.message.answer(
            "Что-то пошло не так, попробуйте зарегистрироваться заново."
        )
        await state.clear()
        return
    await state.update_data(admission_years=admission_years)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=year.year_name, callback_data=str(i))]
            for i, year in enumerate(admission_years)
        ]
    )
    await callback.message.edit_text("Выберите год поступления", reply_markup=keyboard)
    await state.set_state(Register.choosing_year)


@router.callback_query(Register.choosing_year)
async def choosing_year(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        year_id = students_api.get_admission_year_id(
            data["admission_years"],
            data["admission_years"][int(callback.data)].year_name,
        )
        groups = students_api.get_groups(year_id)
    except Exception as e:
        logging.error(e)
        await callback.message.answer(
            "Что-то пошло не так, попробуйте зарегистрироваться заново."
        )
        await state.clear()
        return
    await state.update_data(year_id=year_id, groups=groups)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text=group.student_group_name,
                    callback_data=group.student_group_name,
                )
            ]
            for group in groups
        ]
    )
    await callback.message.edit_text("Выберите группу", reply_markup=keyboard)
    await state.set_state(Register.choosing_group)


@router.callback_query(Register.choosing_group)
async def choosing_group(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    data = await state.get_data()
    try:
        group_id = students_api.get_group_id(data["groups"], callback.data)
    except Exception as e:
        logging.error(e)
        await callback.message.answer(
            "Что-то пошло не так, попробуйте зарегистрироваться заново."
        )
        await state.clear()
        return
    await callback.message.answer(
        f"Номер вашей группы: {group_id}\nВы успешно завершили регистрацию."
    )

    await session.merge(User(telegram_id=callback.from_user.id, group_id=group_id))
    await session.commit()

    await callback.message.delete()
    await state.clear()
