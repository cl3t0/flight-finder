import sqlite3
from find_cities.cacher.cacher_int import AbstractCacher
from datetime import date
from typing import Optional
from result import Result, Ok, Err


class SqliteCacher(AbstractCacher):
    """
    A concrete implementation of the `AbstractCacher` interface that stores data in a SQLite database.

    Args:
        filename (str): The name of the SQLite database file.

    Attributes:
        filename (str): The name of the SQLite database file.
        conn (sqlite3.Connection): A connection to the SQLite database.

    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the SqliteCacher with the given filename.

        Args:
            filename (str): The name of the SQLite database file.
        """
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        SqliteCacher.create_cache_table(self.conn)

    @staticmethod
    def create_cache_table(conn: sqlite3.Connection) -> None:
        """
        Creates the "cache" table in the given SQLite connection, if it does not already exist.

        Args:
            conn (sqlite3.Connection): A connection to the SQLite database.
        """
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS cache(airport1, airport2, chosen_date, price)"
        )

    def store(
        self, airport1: str, airport2: str, chosen_date: date, price: Optional[float]
    ) -> None:
        """
        Stores the given price data for the given airports and chosen date.

        Args:
            airport1 (str): The code of the first airport.
            airport2 (str): The code of the second airport.
            chosen_date (date): The date for which the price is stored.
            price (Optional[float]): The price data to be stored.

        """
        parsed_price = "NULL" if price is None else price
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO cache VALUES"
            f" ('{airport1}', '{airport2}', '{str(chosen_date)}', {parsed_price})"
        )
        self.conn.commit()

    def get(
        self, airport1: str, airport2: str, chosen_date: date
    ) -> Result[Optional[float], str]:
        """
        Retrieves the stored price data for the given airports and chosen date.

        Args:
            airport1 (str): The code of the first airport.
            airport2 (str): The code of the second airport.
            chosen_date (date): The date for which the price data is retrieved.

        Returns:
            Result[Optional[float], str]: The stored price data if it exists, or an error string if it does not.

        """
        cur = self.conn.cursor()
        res = cur.execute(
            "SELECT price FROM cache"
            f" WHERE airport1 = '{airport1}'"
            f" AND airport2 = '{airport2}'"
            f" AND chosen_date = '{str(chosen_date)}'"
        ).fetchall()
        if len(res) == 0:
            return Err("No data")
        else:
            return Ok(res[0][0])
