from datetime import date

import spbu
from spbu.types import SDPLProgramCombination, PGGroup, SDPLAdmissionYear
from typing import List

from consts import divisions_aliases
from views import ExamView, map_exam


def get_study_division_alias(division_name: str) -> str:
    if division_name in divisions_aliases:
        return divisions_aliases[division_name]
    raise Exception("Failed to find study division")


def get_study_levels(alias: str) -> List[str]:
    levels_response = spbu.get_study_levels(alias)
    levels = []
    for level in levels_response:
        levels.append(level.study_level_name)
    return levels


def get_study_level_programs(
    alias: str, study_level: str
) -> List[SDPLProgramCombination]:
    levels = spbu.get_study_levels(alias)
    for level in levels:
        if level.study_level_name == study_level:
            return level.study_program_combinations
    raise Exception("Failed to find study level")


def get_admission_years(
    programs: List[SDPLProgramCombination], program_name: str
) -> List[SDPLAdmissionYear]:
    for program in programs:
        if program.name == program_name:
            return program.admission_years
    raise Exception("Failed to find study program's admission years")


def get_admission_year_id(admission_year: List[SDPLAdmissionYear], year: int) -> str:
    for adm_year in admission_year:
        if adm_year.year_name == str(year):
            return adm_year.study_program_id
    raise Exception("Failed to find study program with this year")


def get_groups(program_id: int) -> List[PGGroup]:
    return spbu.get_groups(program_id)


def get_group_id(groups: List[PGGroup], group_name: str) -> str:
    for group in groups:
        if group.student_group_name == group_name:
            return group.student_group_id
    raise Exception("Failed to find student group")


def get_group_exams(
    group_id: int, from_date: date = None, to_date: date = None
) -> List[ExamView]:
    events = spbu.get_group_events(
        group_id, from_date, to_date, lessons_type=spbu.consts.LessonsTypes.ATTESTATION
    )

    exams = []
    for day in events.days:
        for exam in day.day_study_events:
            exams.append(map_exam(exam))

    return exams
