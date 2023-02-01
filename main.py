from find_cities.airports_table.airports_table_sqlite import SqliteAirportsTable
from find_cities.find import find_best_airport_and_day
from find_cities.api.amadeus_api import AmadeusApi
from find_cities.cacher.sqlite_cacher import SqliteCacher
from find_cities.api.caching_crust import CachingCrust
from decouple import config
from datetime import date

key = config("API_KEY")
secret = config("API_SECRET")
url = config("API_URL")

airports = ["JFK", "GRU", "PHX"]
first_date = date(year=2023, month=3, day=1)
last_date = date(year=2023, month=8, day=1)
cacher = SqliteCacher("cache.db")
client = CachingCrust(AmadeusApi(key, secret, url), cacher)
airports_table = SqliteAirportsTable()

result = find_best_airport_and_day(
    airports,
    client,
    airports_table,
    first_date,
    last_date,
    center_airports_limit=15,
)

print(result)
