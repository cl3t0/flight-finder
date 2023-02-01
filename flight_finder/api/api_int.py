from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Dict, Optional


class AbstractApi(metaclass=ABCMeta):
    """Abstract base class for defining a common interface for flight booking APIs.

    This class defines the methods that a concrete implementation of a flight booking API should provide.
    """

    @abstractmethod
    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Dict[date, Optional[float]]:
        """Get flight prices between two airports for the next 7 days starting from `chosen_date`.

        Args:
            airport1 (str): The IATA code for the first airport
            airport2 (str): The IATA code for the second airport
            chosen_date (date): The starting date for searching for flight prices

        Returns:
            Dict[date, Optional[float]]: A dictionary with keys as dates and values as the corresponding
            flight price between the two airports on that date. If the flight price is not available, the value
            will be `None`.
        """
        pass
