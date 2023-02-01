from find_cities.api.api_int import AbstractApi
from find_cities.cacher.cacher_int import AbstractCacher
from find_cities.api.caching_wrapper import CachingWrapper
from find_cities.utils import date_range
from datetime import date, timedelta
from typing import Dict, Optional, Tuple
from result import Result, Ok, Err


class MockedApi(AbstractApi):
    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, choosen_date: date
    ) -> Dict[date, Optional[float]]:
        data = {
            ("A", "B", date(year=2023, month=1, day=1)): 7,
            ("A", "B", date(year=2023, month=1, day=2)): 5,
            ("A", "B", date(year=2023, month=1, day=3)): 3,
            ("A", "B", date(year=2023, month=1, day=4)): 2,
            ("A", "B", date(year=2023, month=1, day=5)): 3,
            ("A", "B", date(year=2023, month=1, day=6)): 6,
            ("A", "B", date(year=2023, month=1, day=7)): 6,
            #
            ("A", "B", date(year=2023, month=1, day=7 + 1)): 7,
            ("A", "B", date(year=2023, month=1, day=7 + 2)): 5,
            ("A", "B", date(year=2023, month=1, day=7 + 3)): 3,
            ("A", "B", date(year=2023, month=1, day=7 + 4)): 2,
            ("A", "B", date(year=2023, month=1, day=7 + 5)): 3,
            ("A", "B", date(year=2023, month=1, day=7 + 6)): 6,
            ("A", "B", date(year=2023, month=1, day=7 + 7)): 6,
        }
        return {
            day: data[(airport1, airport2, day)]
            for day in date_range(choosen_date, choosen_date + timedelta(days=7))
        }


class InMemoryCacher(AbstractCacher):
    def __init__(self) -> None:
        self.data: Dict[Tuple[str, str, date], Optional[float]] = {}

    def store(
        self, airport1: str, airport2: str, chosen_date: date, price: Optional[float]
    ) -> None:
        self.data[(airport1, airport2, chosen_date)] = price

    def get(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Result[Optional[float], str]:
        key = (airport1, airport2, chosen_date)
        if key in self.data.keys():
            return Ok(self.data[key])
        else:
            return Err("No data")


def test_storage_1():
    cacher = InMemoryCacher()
    client = MockedApi()
    caching_client = CachingWrapper(client, cacher)
    result = caching_client.get_price_between_at_next_7_days(
        "A", "B", date(year=2023, month=1, day=1)
    )
    expected_data_cached = {
        ("A", "B", date(year=2023, month=1, day=1)): 7,
        ("A", "B", date(year=2023, month=1, day=2)): 5,
        ("A", "B", date(year=2023, month=1, day=3)): 3,
        ("A", "B", date(year=2023, month=1, day=4)): 2,
        ("A", "B", date(year=2023, month=1, day=5)): 3,
        ("A", "B", date(year=2023, month=1, day=6)): 6,
        ("A", "B", date(year=2023, month=1, day=7)): 6,
    }
    expected_result = {
        date(year=2023, month=1, day=1): 7,
        date(year=2023, month=1, day=2): 5,
        date(year=2023, month=1, day=3): 3,
        date(year=2023, month=1, day=4): 2,
        date(year=2023, month=1, day=5): 3,
        date(year=2023, month=1, day=6): 6,
        date(year=2023, month=1, day=7): 6,
    }
    assert result == expected_result
    assert cacher.data == expected_data_cached


def test_storage_2():
    cacher = InMemoryCacher()
    client = MockedApi()
    caching_client = CachingWrapper(client, cacher)
    _ = caching_client.get_price_between_at_next_7_days(
        "A", "B", date(year=2023, month=1, day=1)
    )
    result = caching_client.get_price_between_at_next_7_days(
        "A", "B", date(year=2023, month=1, day=3)
    )
    expected_data_cached = {
        ("A", "B", date(year=2023, month=1, day=1)): 7,
        ("A", "B", date(year=2023, month=1, day=2)): 5,
        ("A", "B", date(year=2023, month=1, day=3)): 3,
        ("A", "B", date(year=2023, month=1, day=4)): 2,
        ("A", "B", date(year=2023, month=1, day=5)): 3,
        ("A", "B", date(year=2023, month=1, day=6)): 6,
        ("A", "B", date(year=2023, month=1, day=7)): 6,
        ("A", "B", date(year=2023, month=1, day=7 + 1)): 7,
        ("A", "B", date(year=2023, month=1, day=7 + 2)): 5,
        ("A", "B", date(year=2023, month=1, day=7 + 3)): 3,
        ("A", "B", date(year=2023, month=1, day=7 + 4)): 2,
        ("A", "B", date(year=2023, month=1, day=7 + 5)): 3,
        ("A", "B", date(year=2023, month=1, day=7 + 6)): 6,
        ("A", "B", date(year=2023, month=1, day=7 + 7)): 6,
    }
    expected_result = {
        date(year=2023, month=1, day=3): 3,
        date(year=2023, month=1, day=4): 2,
        date(year=2023, month=1, day=5): 3,
        date(year=2023, month=1, day=6): 6,
        date(year=2023, month=1, day=7): 6,
        date(year=2023, month=1, day=7 + 1): 7,
        date(year=2023, month=1, day=7 + 2): 5,
    }
    assert result == expected_result
    assert cacher.data == expected_data_cached
