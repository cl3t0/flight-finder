from find_cities.sqlite_cacher import SqliteCacher
import pytest
from datetime import date
import os


@pytest.mark.integ
def test_store():
    cacher = SqliteCacher("test.db")
    cacher.store("A", "B", date(year=2020, month=1, day=1), 10)
    os.remove("./test.db")


@pytest.mark.integ
def test_get():
    cacher = SqliteCacher("test.db")
    cacher.store("A", "B", date(year=2020, month=1, day=1), 10)
    result = cacher.get("A", "B", date(year=2020, month=1, day=1))
    assert result == 10
    os.remove("./test.db")
