from flight_finder.airports_table.airports_table_int import AbstractAirportsTable
from flight_finder.mathematics import get_average_coordinate
from flight_finder.api.api_int import AbstractApi
from flight_finder.utils import date_range
from typing import Tuple, List, Dict
from datetime import date, timedelta
import math

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]


class NotListedAirports(Exception):
    """
    Exception to raise when an airport from the input list is not in the all_airports list.

    Args:
        airports (List[str]): List of not listed airports
    """

    def __init__(self, airports: List[str]) -> None:
        super().__init__(str(airports))


def get_average_airports(
    airports: List[str], airports_table: AbstractAirportsTable, limit: int
) -> List[str]:
    """
    Get average coordinate of the given airports and returns closest airports to the average coordinate.

    Args:
        airports (List[str]): List of airports
        airports_table (AbstractAirportsTable): Object to get all the airports and closest airports
        limit (int): Number of closest airports to return

    Returns:
        List[str]: List of closest airports to the average coordinate

    Raises:
        NotListedAirports: If an airport from the input list is not in the all_airports list.
    """
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
    """
    Get travel prices from airport1 to airport2 for the next 7 days starting from `day`.

    Args:
        client (AbstractApi): Object to make API calls to get the travel prices
        airport1 (str): Source airport
        airport2 (str): Destination airport
        day (date): Start day for travel prices

    Returns:
        Dict[date, float]: Dictionary with date as key and travel price as value
    """

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


def find_best_airports_and_days(
    airports: List[str],
    client: AbstractApi,
    airports_table: AbstractAirportsTable,
    from_date: date,
    to_date: date,
    center_airports_limit: int = 10,
    suggestion_quantity: int = 10,
) -> List[Tuple[str, date, float]]:
    """
    This function finds the best airport and date to travel by getting the travel prices of all airports within the
    specified range, then aggregating and choosing the best choice.

    Args:
        airports (List[str]): List of airports to travel from.
        client (AbstractApi): API Client to get travel prices from.
        airports_table (AbstractAirportsTable): Table containing airport information.
        from_date (date): Starting date of travel.
        to_date (date): Ending date of travel.
        center_airports_limit (int): Limit of center airports to get average airport information from.
        suggestion_quantity (int): Length of the output suggestion list

    Returns:
        List[Tuple[str, date, float]]: List of tuples containing the best airports, dates, and travel prices.
    """

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
    ordered_choices = sorted(price_per_choice_agg, key=lambda x: x[2])
    best_choices = ordered_choices[:suggestion_quantity]
    return best_choices
