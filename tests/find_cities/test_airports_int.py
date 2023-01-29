import pytest
from find_cities.airports_int import AirportsInterface


@pytest.mark.integ
def test_get_all_airports():

    interface = AirportsInterface()
    all_airports = interface.get_all()
    assert len(all_airports) != 0
