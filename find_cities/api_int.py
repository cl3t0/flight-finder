from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Dict


class AbstractApi(metaclass=ABCMeta):
    @abstractmethod
    def get_price_between_at_next_7_days(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Dict[date, float]:
        pass
