from dataclasses import dataclass


@dataclass
class UserView:
    telegram_id: int
    group_id: int
    group_name: str
