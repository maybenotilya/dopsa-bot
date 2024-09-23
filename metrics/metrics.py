import logging
import os
from datetime import datetime

from db.manager import DatabaseManager


async def count_metrics(session):
    async with session() as session:
        db_manager = DatabaseManager(session)
        metric = await db_manager.get_number_groups()
    file_mode = "w"
    if os.path.exists(os.environ["DOPSABOT_METRICS_PATH"]):
        file_mode = "a"
    with open(os.environ["DOPSABOT_METRICS_PATH"], file_mode) as f:
        f.write(f"{datetime.now()}: {metric}\n")
