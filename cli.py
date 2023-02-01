from flight_finder.airports_table.airports_table_sqlite import SqliteAirportsTable
from flight_finder.find import find_best_airport_and_day
from flight_finder.api.amadeus_api import AmadeusApi
from flight_finder.cacher.sqlite_cacher import SqliteCacher
from flight_finder.api.caching_wrapper import CachingWrapper
from decouple import config
from datetime import date

key = config("API_KEY")
secret = config("API_SECRET")
url = config("API_URL")

airports = []

while True:
    airport = input("Enter a new airport (Enter an empty string to stop): ")
    if airport == "":
        break
    else:
        airports.append(airport)

first_date = date.fromisoformat(input("Enter the lower bound date: "))
last_date = date.fromisoformat(input("Enter the upper bound date: "))
center_airports_limit = int(input("Enter the center airport limit: "))
cacher = SqliteCacher("cache.db")
client = CachingWrapper(AmadeusApi(key, secret, url), cacher)
airports_table = SqliteAirportsTable()

result = find_best_airport_and_day(
    airports,
    client,
    airports_table,
    first_date,
    last_date,
    center_airports_limit=center_airports_limit,
)

print(result)
