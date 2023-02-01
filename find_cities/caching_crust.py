from find_cities.cacher_int import AbstractCacher
from find_cities.api_int import AbstractApi
from typing import Dict, cast, Optional
from datetime import date, timedelta
from find_cities.utils import date_range


class CachingCrust(AbstractApi):
    def __init__(self, client: AbstractApi, cacher: AbstractCacher) -> None:
        self.client = client
        self.cacher = cacher

    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Dict[date, float]:

        required_data_range = list(
            date_range(chosen_date, chosen_date + timedelta(days=7))
        )

        cached_data = {
            current_date: self.cacher.get(airport1, airport2, current_date)
            for current_date in required_data_range
        }

        if all(price is not None for price in cached_data.values()):
            return cast(Dict[date, float], cached_data)

        first_date = min(
            [
                current_date
                for current_date, price in cached_data.items()
                if price is None
            ]
        )

        result = self.client.get_price_between_at_next_7_days(
            airport1, airport2, first_date
        )
        for current_date, price in result.items():
            self.cacher.store(airport1, airport2, current_date, price)

        cached_plus_result: Dict[date, Optional[float]] = {**cached_data, **result}

        adjusted_output = {
            current_date: cast(float, cached_plus_result[current_date])
            for current_date in required_data_range
            if cached_plus_result[current_date] is not None
        }

        return adjusted_output
