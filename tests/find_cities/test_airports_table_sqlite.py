import pytest
from find_cities.airports_table.airports_table_sqlite import SqliteAirportsTable


@pytest.mark.integ
def test_get_all_airports():

    interface = SqliteAirportsTable()
    all_airports = interface.get_all()
    assert len(all_airports) != 0


@pytest.mark.integ
def test_get_close_airports():

    point = (14.127704, -84.562763)

    interface = SqliteAirportsTable()
    airports = interface.get_close_airports(point, 5)
    assert len(airports) != 0
