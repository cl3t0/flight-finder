from find_cities.airports_table_int import AbstractAirportsTable
from find_cities.mathematics import get_average_coordinate
from find_cities.api.api_int import AbstractApi
from find_cities.utils import date_range
from typing import Tuple, List, Dict
from datetime import date, timedelta
import math

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]


class NotListedAirports(Exception):
    def __init__(self, airports: List[str]) -> None:
        super().__init__(str(airports))


def get_average_airports(
    airports: List[str], airports_table: AbstractAirportsTable, limit: int
) -> List[str]:
    all_airports = airports_table.get_all()

    not_listed_airports = [
        airport for airport in airports if all_airports.get(airport) is None
    ]

    if len(not_listed_airports) != 0:
        raise NotListedAirports(not_listed_airports)

    coordinates = [all_airports[airport] for airport in airports]
    average_coordinate = get_average_coordinate(coordinates)

    return airports_table.get_close_airports(average_coordinate, limit)


def get_travel_price(
    client: AbstractApi, airport1: str, airport2: str, day: date
) -> Dict[date, float]:
    print(f"Getting price from {airport1} to {airport2} at {str(day)}...")

    return (
        {d: 0.0 for d in date_range(day, day + timedelta(days=7))}
        if airport1 == airport2
        else {
            k: v
            for k, v in client.get_price_between_at_next_7_days(
                airport1, airport2, day
            ).items()
            if v is not None
        }
    )


def find_best_airport_and_day(
    airports: List[str],
    client: AbstractApi,
    airports_table: AbstractAirportsTable,
    from_date: date,
    to_date: date,
    center_airports_limit: int = 10,
) -> Tuple[str, date, float]:
    center_airports = get_average_airports(
        airports, airports_table, center_airports_limit
    )
    candidate_airports = center_airports + airports
    print(f"airports: {airports}")
    print(f"candidate_airports: {candidate_airports}")
    price_per_choice = {
        (airport, candidate_airport, current_day): price
        for candidate_airport in candidate_airports
        for airport in airports
        for day in date_range(from_date, to_date, 7)
        for current_day, price in get_travel_price(
            client, airport, candidate_airport, day
        ).items()
    }
    price_per_choice_agg = [
        (
            candidate_airport,
            day,
            sum(
                price_per_choice.get((airport, candidate_airport, day)) or math.inf
                for airport in airports
            ),
        )
        for candidate_airport in candidate_airports
        for day in date_range(from_date, to_date)
    ]
    best_choice = min(price_per_choice_agg, key=lambda x: x[2])
    return best_choice
