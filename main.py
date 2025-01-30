import config
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager
import datetime as dt
from babel import numbers as bn

# Constants
MAX_SEARCH_RESULTS = 10  # Max number of search results to retrieve
INCLUDE_TYPE_IN_SEARCHES = "AIRPORTS"  # Specify search type to include only airports
ADULTS = 1  # Number of passengers to search for

# Query parameters for the home city
HOME_CITY_QUERY = {
    "city": config.city,
    "country": config.country,
    "max": MAX_SEARCH_RESULTS,
    "include": INCLUDE_TYPE_IN_SEARCHES
}

# Initialize objects for various managers
flight_seeker = FlightSearch()
data_manager = DataManager()
flight_data = FlightData()
notification_manager = NotificationManager()

# Step 1: Read data from the user's Google Sheet
locations_data = data_manager.read_cities_data()
print(f"Received Locations data: {locations_data["deals"]}")
email_list = data_manager.get_customer_emails()
print(f"Received emails list: {email_list}")

# Step 2: Get IATA code for the home city
HOME_IATA = flight_seeker.get_city_iata(HOME_CITY_QUERY)
print(f"Home IATA code: {HOME_IATA}")

# Step 3: Ensure IATA codes are set for all destinations
for item in locations_data["deals"]:
    if not item["iataCode"]:  # If IATA code is missing
        city_query = {
            "city": item["city"],
            "max": MAX_SEARCH_RESULTS,
            "include": INCLUDE_TYPE_IN_SEARCHES
        }
        # Retrieve IATA code and update the Google Sheet
        iata = flight_seeker.get_city_iata(city_query)
        item["iataCode"] = iata
        data_manager.set_iata_codes({"id": item["id"], "code": iata})

# Step 4: Define date range for flight searches
today_date = dt.datetime.now().date()
start_date = today_date + dt.timedelta(days=1)  # Flights from tomorrow
return_date = today_date + dt.timedelta(days=180)  # Returning 6 months from today

# Base search parameters for flight searches
flight_search_data = {
    "origin_iata": HOME_IATA,
    "destination_iata": "",
    "adults": ADULTS,
    "departure_date": start_date.strftime("%Y-%m-%d"),
    "return_date": return_date.strftime("%Y-%m-%d"),
    "currency": config.currency
}

# Step 5: Iterate over destinations and find flights
for destination in locations_data["deals"]:
    print(f'Getting flight data for {destination["city"]}')

    # Update search parameters with the destination's IATA code
    search_data = flight_search_data.copy()  # Avoid modifying the base dictionary
    search_data["destination_iata"] = destination["iataCode"]

    # Fetch all possible flights between home city and destination
    all_flights = flight_seeker.get_flights(search_data)
    all_flights_data = all_flights.get("data", [])

    # Determine the cheapest flight
    cheapest_flight = flight_data.get_cheapest_flight(all_flights_data)
    print(f"Cheapest flight found: {cheapest_flight}")

    # Skip the destination if no flights are available
    if cheapest_flight["price"] == "N/A":
        continue

    print("Checking if it meets set criteria...")
    # Check if the cheapest flight is below the user's threshold price
    if float(cheapest_flight["price"]) < float(destination["lowestPrice"]):
        print(f"Flight meets set criteria, sending notification email")
        # send notification emails with flight details

        # Create message: different message for nonstop vs flight with stops
        # Create variables

        price = cheapest_flight["price"]
        symbol = bn.get_currency_symbol(cheapest_flight["currency"], locale='en_US')
        origin = cheapest_flight["origin_airport"]
        destination = cheapest_flight["destination_airport"]
        departure = cheapest_flight["out_date"].split("T")[0]  # Extract only the date portion
        returning = cheapest_flight["return_date"].split("T")[0]  # Extract only the date portion
        if cheapest_flight["stops"] > 0:
            num_stops = f"with {cheapest_flight["stops"]} stop(s)"
        else: num_stops = "non-stop"

        msg = (f"Low price alert! Only {symbol}{price} to fly from {origin} to {destination}, {num_stops}, "
               f"departing on {departure} and returning on {returning}.")

        notification_manager.send_emails(email_list, msg)
