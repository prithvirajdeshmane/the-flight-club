import requests
import os

class FlightSearch:
    """
    This class is responsible for interacting with the Flight Search API
    to fetch city IATA codes and flight offers.
    """

    # API Endpoint URLs
    _AMADEUS_OAUTH2_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
    _AMADEUS_CITYSEARCH_URL = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    _AMADEUS_FLIGHTOFFERS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    # Headers for authentication requests
    _auth_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self):
        """
        Initializes the FlightSearch class by retrieving OAuth2 tokens
        and preparing API headers.
        """
        self._auth_fields = self._get_auth_fields()  # Fields for OAuth2 authentication
        self._api_headers = self._get_api_headers()  # Headers for subsequent API requests

    def _get_auth_fields(self) -> dict:
        """
        Prepares the fields required for OAuth2 authentication.
        Returns:
            dict: The authentication fields containing client ID and secret.
        """
        return {
            "grant_type": "client_credentials",
            "client_id": os.environ.get("AMADEUS_FLIGHTSEARCH_API_KEY"),
            "client_secret": os.environ.get("AMADEUS_FLIGHTSEARCH_API_SECRET"),
        }

    def _get_api_headers(self) -> dict:
        """
        Authenticates with the Amadeus API and retrieves the access token.
        Returns:
            dict: The headers containing the access token for API requests.
        """
        response = requests.post(self._AMADEUS_OAUTH2_URL, headers=self._auth_headers, data=self._auth_fields)
        response.raise_for_status()  # Raise an exception for HTTP errors
        auth_json = response.json()

        # Return headers with the authorization token
        return {
            "Authorization": f"{auth_json['token_type']} {auth_json['access_token']}"
        }

    def get_city_iata(self, data) -> str:
        """
        Fetches the IATA code for a city.
        Args:
            data (dict): Dictionary containing city search parameters.
        Returns:
            str: The IATA code for the city.
        """
        city_config = {
            "keyword": data["city"],  # City name to search for
            "max": data["max"],       # Max number of results to retrieve
            "include": data["include"]  # Type of locations to include
        }

        # Add country code if provided
        if "country" in data and data["country"]:
            city_config["countryCode"] = data["country"]

        try:
            response = requests.get(
                self._AMADEUS_CITYSEARCH_URL,
                headers=self._api_headers,
                params=city_config
            )
            response.raise_for_status()
            city_data = response.json()

            # Return the first matching city's IATA code
            return city_data["data"][0]["iataCode"]

        except KeyError:
            print("Error: City not found. Please verify the provided data.")
        except IndexError:
            print("Error: No city data returned by the API.")
        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")

    def get_flights(self, flight_search_data, is_direct = True) -> dict:
        """
        Fetches flight offers based on search parameters.
        First searches for non-stop flights only, if none are found,
        then looks for flights with layovers
        Args:
            flight_search_data (dict): Dictionary containing flight search parameters.
            is_direct (bool): Determines whether to check for non-stop flight or flights with stops
        Returns:
            dict: The flight data retrieved from the API.
        """

        # Prepare the query parameters for the flight offers API
        query = {
            "originLocationCode": flight_search_data["origin_iata"],
            "destinationLocationCode": flight_search_data["destination_iata"],
            "departureDate": flight_search_data["departure_date"],
            "returnDate": flight_search_data["return_date"],
            "adults": flight_search_data["adults"],
            "nonStop": str(is_direct).lower(),
            "currencyCode": flight_search_data["currency"]
        }

        try:
            # API call to fetch flight offers
            response = requests.get(
                self._AMADEUS_FLIGHTOFFERS_URL,
                headers=self._api_headers,
                params=query
            )
            response.raise_for_status()
            data = response.json()

            # If there are no direct flights found, then look for indirect flights
            if len(data["data"]) == 0:
                data = self.get_flights(flight_search_data, False)

            # return list of flights found
            return data

        except requests.exceptions.RequestException as e:
            print(f"Error during API call for flight offers: {e}")
            return {}
