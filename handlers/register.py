import logging

from aiogram import Bot, F, Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from consts import BotCommands, divisions_aliases, Messages
from db.manager import DatabaseManager
from notifier.notifier import notify
from timetable_api import students_api
from formatters import format_exams


class ChoosingOccupation(StatesGroup):
    choosing_occupation = State()


class StudentRegister(StatesGroup):
    choosing_division = State()
    choosing_level = State()
    choosing_year = State()
    choosing_program = State()
    choosing_group = State()


class EducatorRegister(StatesGroup):
    choosing_educator = State()


router = Router()


@router.message(StateFilter(None), Command(BotCommands.exit))
async def exit(message: types.Message):
    await message.answer("Вы не регистрируетесь, отменять нечего.")


@router.message(Command(BotCommands.exit))
async def exit(message: types.Message, state: FSMContext):
    await message.answer("Отменяю вашу регистрацию.")
    await state.clear()


@router.message(Command(BotCommands.register))
async def register(message: types.Message, state: FSMContext):
    keyboard = keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=occupation, callback_data=occupation)]
            for occupation in ["Студент", "Преподаватель"]
        ]
    )
    await message.answer("Выберите кто вы", reply_markup=keyboard)
    await state.set_state(ChoosingOccupation.choosing_occupation)


@router.callback_query(
    ChoosingOccupation.choosing_occupation, F.data == "Преподаватель"
)
async def educator_register(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Извините, но я пока не сделял")
    await callback.message.delete()


@router.callback_query(ChoosingOccupation.choosing_occupation, F.data == "Студент")
async def student_register(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(Messages.loading_message)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=k, callback_data=v)]
            for k, v in divisions_aliases.items()
        ]
    )
    await callback.message.edit_text(
        "Выберите название вашего факультета.", reply_markup=keyboard
    )
    await state.set_state(StudentRegister.choosing_division)


@router.callback_query(StudentRegister.choosing_division)
async def choosing_division(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(Messages.loading_message)
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
    await state.set_state(StudentRegister.choosing_level)


@router.callback_query(StudentRegister.choosing_level)
async def choosing_level(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await callback.message.edit_text(Messages.loading_message)
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
    await state.set_state(StudentRegister.choosing_program)


@router.callback_query(StudentRegister.choosing_program)
async def choosing_program(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await callback.message.edit_text(Messages.loading_message)
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
    await state.set_state(StudentRegister.choosing_year)


@router.callback_query(StudentRegister.choosing_year)
async def choosing_year(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        await callback.message.edit_text(Messages.loading_message)
        year_id = students_api.get_admission_year_id(
            data["admission_years"],
            int(data["admission_years"][int(callback.data)].year_name),
        )
        year_id = int(year_id)
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
    await state.set_state(StudentRegister.choosing_group)


@router.callback_query(StudentRegister.choosing_group)
async def choosing_group(
    callback: types.CallbackQuery,
    state: FSMContext,
    db_manager: DatabaseManager,
    bot: Bot,
):
    data = await state.get_data()
    try:
        await callback.message.edit_text(Messages.loading_message)
        group_id = int(students_api.get_group_id(data["groups"], callback.data))
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

    await db_manager.insert_group(group_id, callback.data)
    await notify(bot, db_manager)

    await db_manager.upsert_user(callback.from_user.id, group_id, callback.data)
    logging.info(
        f"User id: {callback.from_user.id}, group: {group_id}, group name: {callback.data}"
    )

    exams = await db_manager.get_exams()
    if len(exams[group_id]) == 0:
        await callback.message.answer(Messages.no_exams_message)
    else:
        message_text = Messages.month_exams_message + format_exams(exams[group_id])
        await callback.message.answer(message_text)

    await callback.message.delete()
    await state.clear()


@router.message(Command(BotCommands.unregister))
async def unregister(message: types.Message, db_manager: DatabaseManager):
    await db_manager.delete_user(message.from_user.id)
    await message.answer(Messages.unnregister_message)
