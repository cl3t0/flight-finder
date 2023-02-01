from find_cities.cacher_int import AbstractCacher
from find_cities.api_int import AbstractApi
from typing import Dict, Optional
from datetime import date, timedelta
from find_cities.utils import date_range
from result import Ok, Err


class CachingCrust(AbstractApi):
    def __init__(self, client: AbstractApi, cacher: AbstractCacher) -> None:
        self.client = client
        self.cacher = cacher

    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Dict[date, Optional[float]]:

        required_data_range = list(
            date_range(chosen_date, chosen_date + timedelta(days=7))
        )

        cached_data = {
            current_date: self.cacher.get(airport1, airport2, current_date)
            for current_date in required_data_range
        }
        ok_cached_data = {
            day: price.value
            for day, price in cached_data.items()
            if isinstance(price, Ok)
        }

        if len(ok_cached_data) == len(cached_data):
            print("Using cached data.")
            return ok_cached_data
        print("Requesting data from API...")

        first_date = min(
            [
                current_date
                for current_date, price in cached_data.items()
                if isinstance(price, Err)
            ]
        )

        result = self.client.get_price_between_at_next_7_days(
            airport1, airport2, first_date
        )
        for current_date, price in result.items():
            self.cacher.store(airport1, airport2, current_date, price)

        cached_plus_result: Dict[date, Optional[float]] = {**ok_cached_data, **result}

        adjusted_output = {
            current_date: cached_plus_result[current_date]
            for current_date in required_data_range
        }

        return adjusted_output
