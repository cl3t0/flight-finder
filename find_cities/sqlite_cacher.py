import sqlite3
from find_cities.cacher_int import AbstractCacher
from datetime import date
from typing import Optional
from result import Result, Ok, Err


class SqliteCacher(AbstractCacher):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        SqliteCacher.create_cache_table(self.conn)

    @staticmethod
    def create_cache_table(conn: sqlite3.Connection) -> None:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS cache(airport1, airport2, chosen_date, price)"
        )

    def store(
        self, airport1: str, airport2: str, chosen_date: date, price: Optional[float]
    ) -> None:
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
