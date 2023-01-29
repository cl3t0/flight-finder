import sqlite3
from typing import Tuple, Dict


class AirportsInterface:
    def __init__(self) -> None:

        self.conn = sqlite3.connect("global_airports_sqlite.db")

    def get_all(self) -> Dict[str, Tuple[float, float]]:
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT iata_code, lat_decimal, lon_decimal FROM airports"
            " WHERE iata_code != 'N/A'"
            " AND lat_decimal != 0"
            " AND lon_decimal != 0"
        )

        return {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
