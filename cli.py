from flight_finder.airports_table.airports_table_sqlite import SqliteAirportsTable
from flight_finder.find import find_best_airports_and_days
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
center_airports_limit = int(input("Enter the center airports limit: "))
suggestion_quantity = int(input("Enter how much flight suggestions do you want: "))

cacher = SqliteCacher("cache/cache.db")
client = CachingWrapper(AmadeusApi(key, secret, url), cacher)
airports_table = SqliteAirportsTable()

results = find_best_airports_and_days(
    airports,
    client,
    airports_table,
    first_date,
    last_date,
    center_airports_limit=center_airports_limit,
    suggestion_quantity=suggestion_quantity,
)

print("Results:")

for i, (airport, day, price) in enumerate(results):
    print(f"(Option {i})")
    print(f"- Airport: {airport}")
    print(f"- Date: {day}")
    print(f"- Total price: {price}")
