from typing import Tuple, Dict, List
from abc import ABCMeta, abstractmethod


class AbstractAirportsTable(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> Dict[str, Tuple[float, float]]:
        pass

    @abstractmethod
    def get_close_airports(self, point: Tuple[float, float], limit: int) -> List[str]:
        pass
