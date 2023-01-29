import pytest
from find_cities.amadeus_api import AmadeusApi
from decouple import config
from datetime import date


@pytest.mark.integ
def test_check_price_between_gru_and_cnf():

    key = config("API_KEY")
    secret = config("API_SECRET")
    url = config("API_URL")

    client = AmadeusApi(key, secret, url)
    price = client.get_price_between_at_next_7_days(
        "GRU", "CNF", date(year=2023, month=4, day=1)
    )
    assert len(price) > 0
