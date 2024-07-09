from dataclasses import dataclass
from typing import List

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
