from dataclasses import dataclass
from datetime import datetime

from spbu.types import GEEvent


@dataclass
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
        educators=event.educators_display_text,
    )
