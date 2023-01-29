from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Dict


class AbstractApi(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, key: str, secret: str, url: str) -> None:
        pass

    @abstractmethod
    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, date: date
    ) -> Dict[date, float]:
        pass
