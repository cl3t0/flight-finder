from find_cities.find import get_average_airports, find_best_airport_and_day
from find_cities.airports_table_int import AbstractAirportsTable
from find_cities.api_int import AbstractApi
from find_cities.utils import date_range
from typing import Tuple, Dict, List, Optional
from datetime import date, timedelta


class MockedAirportsTable(AbstractAirportsTable):
    def get_all(self) -> Dict[str, Tuple[float, float]]:
        return {
            "A": (0.0, 0.0),
            "B": (0.0, -45.0),
            "C": (0.0, 45.0),
            "D": (90.0, 0.0),
            "E": (60.0, 0.0),
        }

    def get_close_airports(self, point: Tuple[float, float], limit: int) -> List[str]:
        return {(35.264389682754654, 0.0): ["E", "A", "B", "C", "D"]}[point][:limit]


class MockedApi(AbstractApi):
    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, choosen_date: date
    ) -> Dict[date, Optional[float]]:
        data = {
            # B -> E
            ("B", "E", date(year=2023, month=1, day=1)): 2,
            ("B", "E", date(year=2023, month=1, day=2)): 7,
            ("B", "E", date(year=2023, month=1, day=3)): 3,
            ("B", "E", date(year=2023, month=1, day=4)): 3,
            ("B", "E", date(year=2023, month=1, day=5)): 5,
            ("B", "E", date(year=2023, month=1, day=6)): 4,
            ("B", "E", date(year=2023, month=1, day=7)): 7,
            # B -> A
            ("B", "A", date(year=2023, month=1, day=1)): 7,
            ("B", "A", date(year=2023, month=1, day=2)): 5,
            ("B", "A", date(year=2023, month=1, day=3)): 3,
            ("B", "A", date(year=2023, month=1, day=4)): 2,
            ("B", "A", date(year=2023, month=1, day=5)): 3,
            ("B", "A", date(year=2023, month=1, day=6)): 6,
            ("B", "A", date(year=2023, month=1, day=7)): 6,
            # C -> E
            ("C", "E", date(year=2023, month=1, day=1)): 2,
            ("C", "E", date(year=2023, month=1, day=2)): 2,
            ("C", "E", date(year=2023, month=1, day=3)): 4,
            ("C", "E", date(year=2023, month=1, day=4)): 7,
            ("C", "E", date(year=2023, month=1, day=5)): 5,
            ("C", "E", date(year=2023, month=1, day=6)): 6,
            ("C", "E", date(year=2023, month=1, day=7)): 8,
            # C -> A
            ("C", "A", date(year=2023, month=1, day=1)): 2,
            ("C", "A", date(year=2023, month=1, day=2)): 5,
            ("C", "A", date(year=2023, month=1, day=3)): 3,
            ("C", "A", date(year=2023, month=1, day=4)): 7,
            ("C", "A", date(year=2023, month=1, day=5)): 3,
            ("C", "A", date(year=2023, month=1, day=6)): 6,
            ("C", "A", date(year=2023, month=1, day=7)): 2,
            # D -> E
            ("D", "E", date(year=2023, month=1, day=1)): 9,
            ("D", "E", date(year=2023, month=1, day=2)): 5,
            ("D", "E", date(year=2023, month=1, day=3)): 7,
            ("D", "E", date(year=2023, month=1, day=4)): 8,
            ("D", "E", date(year=2023, month=1, day=5)): 5,
            ("D", "E", date(year=2023, month=1, day=6)): 1,
            ("D", "E", date(year=2023, month=1, day=7)): 8,
            # D -> A
            ("D", "A", date(year=2023, month=1, day=1)): 8,
            ("D", "A", date(year=2023, month=1, day=2)): 2,
            ("D", "A", date(year=2023, month=1, day=3)): 4,
            ("D", "A", date(year=2023, month=1, day=4)): 5,
            ("D", "A", date(year=2023, month=1, day=5)): 8,
            ("D", "A", date(year=2023, month=1, day=6)): 2,
            ("D", "A", date(year=2023, month=1, day=7)): 1,
            # E - 1 => 2 + 2 + 9 = 13
            # E - 2 => 7 + 2 + 5 = 14
            # E - 3 => 3 + 4 + 7 = 14
            # E - 4 => 3 + 7 + 8 = 18
            # E - 5 => 5 + 5 + 5 = 15
            # E - 6 => 4 + 6 + 1 = 11
            # E - 7 => 7 + 8 + 8 = 23
            # A - 1 => 7 + 2 + 8 = 17
            # A - 2 => 5 + 5 + 2 = 12
            # A - 3 => 3 + 3 + 4 = 10
            # A - 4 => 2 + 7 + 5 = 14
            # A - 5 => 3 + 3 + 8 = 14
            # A - 6 => 6 + 6 + 2 = 14
            # A - 7 => 6 + 2 + 1 = 9  <-------
        }
        return {
            day: data.get((airport1, airport2, day))
            for day in date_range(choosen_date, choosen_date + timedelta(days=7))
        }


def test_get_average_airports():
    airports_table = MockedAirportsTable()
    airports = ["B", "C", "D"]
    result = get_average_airports(airports, airports_table, 2)
    assert result == ["E", "A"]


def test_find_best_airport_and_day():
    airports_table = MockedAirportsTable()
    client = MockedApi()
    airports = ["B", "C", "D"]
    start_date = date(year=2023, month=1, day=1)
    end_date = date(year=2023, month=1, day=8)
    result = find_best_airport_and_day(
        airports, client, airports_table, start_date, end_date, 2
    )
    assert result == ("A", date(year=2023, month=1, day=7), 9)
