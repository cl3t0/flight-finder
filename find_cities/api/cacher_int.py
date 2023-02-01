from abc import ABCMeta, abstractmethod
from typing import Optional
from datetime import date
from result import Result


class AbstractCacher(metaclass=ABCMeta):
    """
    An abstract class for a cache. A cache stores a price for a given route and date,
    and allows for retrieving the stored price.
    """

    @abstractmethod
    def store(
        self, airport1: str, airport2: str, chosen_date: date, price: Optional[float]
    ) -> None:
        """
        Store a price for a given route and date.

        Args:
            airport1 (str): The departure airport.
            airport2 (str): The destination airport.
            chosen_date (date): The date of departure.
            price (Optional[float]): The price for the route and date, if available.

        Returns:
            None
        """
        pass

    @abstractmethod
    def get(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Result[Optional[float], str]:
        """
        Retrieve the stored price for a given route and date.

        Args:
            airport1 (str): The departure airport.
            airport2 (str): The destination airport.
            chosen_date (date): The date of departure.

        Returns:
            Result[Optional[float], str]: A Result object holding the stored price or an error message.
        """
        pass
