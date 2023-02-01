from flight_finder.api.api_int import AbstractApi
from flight_finder.utils import date_range
from typing import List, Dict, TypedDict, Optional
from datetime import date, timedelta, datetime
import requests


class FlightData(TypedDict):
    """A typed dictionary representing flight data."""

    price: Dict[str, str]
    itineraries: List[Dict[str, List[Dict[str, Dict[str, str]]]]]


class AmadeusApi(AbstractApi):
    """A concrete implementation of the abstract API class for retrieving flight information from the Amadeus API."""

    class MissingFieldError(Exception):
        """Raised when a required field is missing in the API response."""

        pass

    class BadStatusCode(Exception):
        """Raised when the API returns a non-200 status code.

        Attributes:
            status_code (int): The returned status code.
            message (bytes): The error message.
        """

        def __init__(self, status_code: int, message: bytes) -> None:
            super().__init__(f"{status_code}: {str(message)}")

    class NoItineraryError(Exception):
        """Raised when no itinerary is found in the API response."""

        def __init__(self) -> None:
            super().__init__("")

    class NoSegmentError(Exception):
        """Raised when no segment is found in the API response."""

        def __init__(self) -> None:
            super().__init__("")

    token_route = "v1/security/oauth2/token"
    main_route = "v2/shopping/flight-offers"

    def __init__(self, key: str, secret: str, url: str) -> None:
        """Initialize the AmadeusApi object.

        Args:
            key (str): The API key.
            secret (str): The API secret.
            url (str): The API base URL.
        """
        self.key = key
        self.secret = secret
        self.url = url
        self.access_token = AmadeusApi.get_token(
            f"{self.url}/{self.token_route}", key, secret
        )

    @staticmethod
    def get_token(url: str, key: str, secret: str) -> str:
        """Get an access token from the API.

        Args:
            url (str): The URL to get the access token from.
            key (str): The API key.
            secret (str): The API secret.

        Returns:
            str: The access token.

        Raises:
            AmadeusApi.BadStatusCode: If the API returns a non-200 status code.
            AmadeusApi.MissingFieldError: If the 'access_token' field is missing in the API response.
        """
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

    @staticmethod
    def make_custom_req(
        url: str,
        access_token: str,
        origin_airport: str,
        destination_airport: str,
        central_date: date,
    ) -> requests.Response:
        """
        A helper method to make API requests to Amadeus API.

        Args:
            url (str): API endpoint URL.
            access_token (str): API access token.
            origin_airport (str): Origin airport code.
            destination_airport (str): Destination airport code.
            central_date (date): Date in the middle of the date range for flight search.

        Returns:
            requests.Response: API response.
        """
        response = requests.post(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "currencyCode": "USD",
                "originDestinations": [
                    {
                        "id": "1",
                        "originLocationCode": origin_airport,
                        "destinationLocationCode": destination_airport,
                        "arrivalDateTimeRange": {
                            "date": str(central_date),
                            "dateWindow": "I3D",
                        },
                    }
                ],
                "travelers": [{"id": "1", "travelerType": "ADULT"}],
                "sources": ["GDS"],
                "searchCriteria": {"oneFlightOfferPerDay": True, "maxFlightOffers": 7},
            },
        )

        return response

    def get_price_between_at_next_7_days(
        self, origin_airport: str, destination_airport: str, chosen_date: date
    ) -> Dict[date, Optional[float]]:
        """
        A method to get the price of flights between two airports in the next 7 days.

        Args:
            origin_airport (str): Origin airport code.
            destination_airport (str): Destination airport code.
            chosen_date (date): Date to start the date range for flight search.

        Returns:
            Dict[date, Optional[float]]: A dictionary where keys are dates and values are the corresponding flight price.

        Raises:
            AmadeusApi.BadStatusCode: If the API returns a non-200 status code.
            AmadeusApi.MissingFieldError: If some field is missing in the API response.
            AmadeusApi.NoItineraryError: If the "itineraries" field is found but has no elements.
            AmadeusApi.NoSegmentError: If the "segments" field is found but has no elements.
        """

        central_date = chosen_date + timedelta(days=3)

        response = AmadeusApi.make_custom_req(
            f"{self.url}/{self.main_route}",
            self.access_token,
            origin_airport,
            destination_airport,
            central_date,
        )

        if response.status_code == 401:
            self.access_token = AmadeusApi.get_token(
                f"{self.url}/{self.token_route}", self.key, self.secret
            )
            response = AmadeusApi.make_custom_req(
                f"{self.url}/{self.main_route}",
                self.access_token,
                origin_airport,
                destination_airport,
                central_date,
            )

        if response.status_code != 200:
            raise AmadeusApi.BadStatusCode(response.status_code, response.content)

        response_json: Dict[str, List[FlightData]] = response.json()

        data = response_json.get("data")

        if data is None:
            raise AmadeusApi.MissingFieldError("data")

        result = {}

        for flight in data:
            itineraries = flight.get("itineraries")

            if itineraries is None:
                raise AmadeusApi.MissingFieldError("itineraries")

            if len(itineraries) == 0:
                raise AmadeusApi.NoItineraryError()

            itinerary = itineraries[-1]
            segments = itinerary.get("segments")

            if segments is None:
                raise AmadeusApi.MissingFieldError("segments")

            if len(segments) == 0:
                raise AmadeusApi.NoSegmentError()

            segment = segments[-1]
            arrival = segment.get("arrival")

            if arrival is None:
                raise AmadeusApi.MissingFieldError("arrival")

            at = arrival.get("at")

            if at is None:
                raise AmadeusApi.MissingFieldError("at")

            price = flight.get("price")

            if price is None:
                raise AmadeusApi.MissingFieldError("price")

            total = price.get("total")

            if total is None:
                raise AmadeusApi.MissingFieldError("total")

            parsed_at = datetime.fromisoformat(at).date()
            parsed_total = float(total)

            result[parsed_at] = parsed_total

        return {
            day: result.get(day)
            for day in date_range(chosen_date, chosen_date + timedelta(days=7))
        }
