from datetime import date, timedelta
from typing import Generator


def date_range(
    start_date: date, end_date: date, step: int = 1
) -> Generator[date, None, None]:
    for n in range(0, int((end_date - start_date).days), step):
        yield start_date + timedelta(n)
