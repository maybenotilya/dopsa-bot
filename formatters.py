from typing import List

from views import ExamView

date_format = "%d.%m.%Y"
time_format = "%H:%M"


def format_exams(exams: List[ExamView]) -> str:
    message = ""
    for exam in exams:
        message += f"\n\n📚  {exam.subject}\n⏰  {exam.start.strftime(date_format)}  {exam.start.strftime(time_format)} - {exam.end.strftime(time_format)}\n🏠  {exam.address}\n🧑‍🏫   {exam.educator}"

    return message
