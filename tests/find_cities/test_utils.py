from find_cities.utils import date_range
from datetime import date


def test_date_range_1():
    start_date = date(year=2023, month=1, day=1)
    end_date = date(year=2023, month=1, day=4)
    result = date_range(start_date, end_date)
    assert list(result) == [
        date(year=2023, month=1, day=1),
        date(year=2023, month=1, day=2),
        date(year=2023, month=1, day=3),
    ]


def test_date_range_2():
    start_date = date(year=2023, month=1, day=1)
    end_date = date(year=2023, month=1, day=6)
    result = date_range(start_date, end_date, 2)
    assert list(result) == [
        date(year=2023, month=1, day=1),
        date(year=2023, month=1, day=3),
        date(year=2023, month=1, day=5),
    ]
