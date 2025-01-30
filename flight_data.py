class FlightData:
    """
    This class is responsible for structuring and processing flight data,
    particularly for finding the cheapest flight.
    """

    def __init__(self):
        """
        Initializes the FlightData class with a default structure for the cheapest flight.
        """
        self.cheapest_flight = {
            "price": "N/A",
            "origin_airport": "N/A",
            "destination_airport": "N/A",
            "out_date": "N/A",
            "return_date": "N/A",
            "currency": "N/A",
            "stops" : "N/A"
        }

    def get_cheapest_flight(self, data):
        """
        Determines the cheapest flight from a list of flight options.
        Args:
            data (list): A list of flight data dictionaries.
        Returns:
            dict: Details of the cheapest flight.
        """
        # If no flight data is available, return the default cheapest flight
        if not data or len(data) == 0:
            return self.cheapest_flight

        # Initialize with the first flight as the cheapest
        self._mark_cheapest_flight(data[0])

        # Iterate through all flights to find the cheapest one
        for flight in data:
            try:
                # Compare flight prices to find the cheapest
                if float(flight["price"]["grandTotal"]) < float(self.cheapest_flight["price"]):
                    self._mark_cheapest_flight(flight)
            except (KeyError, ValueError) as e:
                # Handle missing or invalid price data gracefully
                print(f"Error processing flight data: {e}")

        # Return details of the cheapest flight
        return self.cheapest_flight

    def _mark_cheapest_flight(self, info):
        """
        Updates the details of the cheapest flight.
        Args:
            info (dict): A dictionary containing details of a flight.
        """
        try:
            self.cheapest_flight = {
                "price": info["price"]["grandTotal"],
                "origin_airport": info["itineraries"][0]["segments"][0]["departure"]["iataCode"],
                "destination_airport": info["itineraries"][1]["segments"][0]["departure"]["iataCode"],
                "out_date": info["itineraries"][0]["segments"][0]["departure"]["at"],
                "return_date": info["itineraries"][1]["segments"][0]["departure"]["at"],
                "currency": info["price"]["currency"],
                "stops": len(info["itineraries"][0]["segments"]) - 1
            }
        except KeyError as e:
            # Log errors if any required keys are missing
            print(f"Error extracting flight details: {e}")
