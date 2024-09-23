import logging

from datetime import date, timedelta
from aiogram import Bot

from db.manager import DatabaseManager
from timetable_api.students_api import get_group_exams
from formatters import format_exams
from consts import Messages


async def notify(bot: Bot, db_manager: DatabaseManager):
    groups = await db_manager.get_groups()
    exams = await db_manager.get_exams()
    for group in groups:
        group_exams = get_group_exams(
            group_id=group.group_id,
            from_date=date.today(),
            to_date=date.today() + timedelta(days=28),
        )
        new_exams = set(group_exams) - set(exams.get(group.group_id, []))
        if len(new_exams) != 0:
            new_exams = list(new_exams)
            message = Messages.new_exams_messages + format_exams(new_exams)
            for user in group.users:
                await bot.send_message(user.telegram_id, message)

        exams[group.group_id] = group_exams
    await db_manager.dumb_exams(exams)


async def scheduled_notify(bot: Bot, session):
    async with session() as session:
        db_manager = DatabaseManager(session)
        await notify(bot, db_manager)
