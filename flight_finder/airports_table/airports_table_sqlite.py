import sqlite3
from typing import Tuple, Dict, List
from flight_finder.airports_table.airports_table_int import AbstractAirportsTable


class SqliteAirportsTable(AbstractAirportsTable):
    def __init__(self) -> None:

        self.conn = sqlite3.connect("global_airports_sqlite.db")
        self.conn.create_function("POW", 2, lambda x, y: x**y)

    def get_all(self) -> Dict[str, Tuple[float, float]]:
        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT iata_code, lat_decimal, lon_decimal FROM airports"
            " WHERE iata_code != 'N/A'"
            " AND lat_decimal != 0"
            " AND lon_decimal != 0"
        )

        return {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    def get_close_airports(self, point: Tuple[float, float], limit: int) -> List[str]:
        lat, long = point

        cursor = self.conn.cursor()

        cursor.execute(
            "SELECT iata_code FROM airports"
            " WHERE iata_code != 'N/A'"
            " AND lat_decimal != 0"
            " AND lon_decimal != 0"
            f" ORDER BY POW(POW(lat_decimal - {lat}, 2) + POW(lon_decimal - {long}, 2), 0.5)"
            f" LIMIT {limit}"
        )

        return [row[0] for row in cursor.fetchall()]
