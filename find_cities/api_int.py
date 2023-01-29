from abc import ABCMeta, abstractmethod
from datetime import date


class AbstractApi(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, key: str, secret: str, url: str) -> None:
        pass

    @abstractmethod
    def get_price_between(self, airport1: str, airport2: str, date: date) -> float:
        pass
