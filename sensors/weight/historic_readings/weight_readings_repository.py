import os
from datetime import datetime
from typing import Collection

__db_file_path__ = os.getcwd() + "/weight_readings.db"

def get_latest_readings(take: int) -> list[str]:
    if not take:
        return []

    # lets skip potential perf issues for now
    with open(__db_file_path__, "r") as file:
        lines = file.readlines()
        return list(
            map(
                lambda x: (x.split("-")[0], float(x.split("-")[1])),
                lines[-take:]
            )
        )

def save_new_reading(reading: float) ->  tuple[str, float]:
    if not reading:
        return

    with open(__db_file_path__, "a") as file:
        id = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        file.writelines(f"{id}-{reading}\n")
        return (id, reading)