from find_cities.api_int import AbstractApi
from typing import List, Optional, Dict
from datetime import date
import requests


class AmadeusApi(AbstractApi):
    class MissingFieldError(Exception):
        pass

    class BadStatusCode(Exception):
        def __init__(self, status_code: int, message: str) -> None:
            super().__init__(f"{status_code}: {message}")

    class NotFlightError(Exception):
        def __init__(self) -> None:
            super().__init__("")

    token_route = "v1/security/oauth2/token"
    main_route = "v2/shopping/flight-offers"

    def __init__(self, key: str, secret: str, url: str) -> None:
        self.key = key
        self.secret = secret
        self.url = url
        self.access_token = AmadeusApi.get_token(
            f"{self.url}/{self.token_route}", key, secret
        )

    @staticmethod
    def get_token(url: str, key: str, secret: str) -> str:
        response = requests.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type=client_credentials&client_id={key}&client_secret={secret}",
        )

        if response.status_code != 200:
            raise AmadeusApi.BadStatusCode(response.status_code, response.content)

        response_json: Dict[str, str] = response.json()

        access_token = response_json.get("access_token")

        if access_token is None:
            raise AmadeusApi.MissingFieldError("access_token")

        return access_token

    def get_price_between(
        self, origin_airport: str, destination_airport: str, date: date
    ) -> float:
        response = requests.post(
            f"{self.url}/{self.main_route}",
            headers={"Authorization": f"Bearer {self.access_token}"},
            json={
                "currencyCode": "USD",
                "originDestinations": [
                    {
                        "id": "1",
                        "originLocationCode": origin_airport,
                        "destinationLocationCode": destination_airport,
                        "arrivalDateTimeRange": {
                            "date": str(date),
                            "dateWindow": "M3D",
                        },
                    }
                ],
                "travelers": [{"id": "1", "travelerType": "ADULT"}],
                "sources": ["GDS"],
                "searchCriteria": {"maxFlightOffers": 1},
            },
        )

        if response.status_code != 200:
            raise AmadeusApi.BadStatusCode(response.status_code, response.content)

        response_json: Dict[str, List[Dict[str, Dict[str, str]]]] = response.json()

        data = response_json.get("data")

        if data is None:
            raise AmadeusApi.MissingFieldError("data")

        if len(data) == 0:
            raise AmadeusApi.NotFlightError()

        flight = data[0]
        price = flight.get("price")

        if price is None:
            raise AmadeusApi.MissingFieldError("price")

        total = price.get("total")

        if total is None:
            raise AmadeusApi.MissingFieldError("total")

        return float(total)
