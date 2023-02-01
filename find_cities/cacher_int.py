from abc import ABCMeta, abstractmethod
from typing import Optional
from datetime import date


class AbstractCacher(metaclass=ABCMeta):
    @abstractmethod
    def store(
        self, airport1: str, airport2: str, chosen_date: date, price: float
    ) -> None:
        pass

    @abstractmethod
    def get(self, airport1: str, airport2: str, chosen_date: date) -> Optional[float]:
        pass
