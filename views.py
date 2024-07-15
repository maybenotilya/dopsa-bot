from dataclasses import dataclass
from datetime import datetime
from typing import List
from spbu.types import GEEvent

from db.models import User, Group


@dataclass
class UserView:
    telegram_id: int
    group_id: int


@dataclass
class GroupView:
    group_id: int
    group_name: str
    users: List[UserView]


def map_user(user: User) -> UserView:
    return UserView(telegram_id=user.telegram_id, group_id=user.group_id)


def map_group(group: Group) -> GroupView:
    return GroupView(
        group_id=group.group_id,
        group_name=group.group_name,
        users=[map_user(user) for user in group.users],
    )


@dataclass(frozen=True)
class ExamView:
    subject: str
    start: datetime
    end: datetime
    address: str
    educator: str


def map_exam(event: GEEvent) -> ExamView:
    return ExamView(
        subject=event.subject,
        start=event.start,
        end=event.end,
        address=event.locations_display_text,
        educator=event.educators_display_text,
    )
