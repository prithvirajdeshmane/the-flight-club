import os
import requests

class DataManager:
    """
    This class is responsible for interacting with the Google Sheet
    containing flight deals using the Sheety API.
    """

    def __init__(self):
        """
        Initializes the DataManager class with the API URL and headers.
        """
        self.deals_api_url = os.environ.get("SHEETY_FLIGHTDEALS_URL")  # Base URL for Sheety API - Deals
        self.users_api_url = os.environ.get("SHEETY_FLIGHTDEALS_USERS_URL") # Base URL for Sheety API - Users
        self.api_headers = {
            "Authorization": f"Bearer {os.environ.get('SHEETY_BEARER_TOKEN')}"  # Bearer token for authentication
        }

    def set_iata_codes(self, data):
        """
        Updates the IATA code for a specific city in the Google Sheet.
        Args:
            data (dict): A dictionary containing the city ID and IATA code.
                Example: {"id": 2, "code": "LHR"}
        """
        update_row_url = f"{self.deals_api_url}/{data['id']}"  # URL for updating a specific row
        body = {
            "deal": {
                "iataCode": data["code"],  # Update the IATA code in the 'deal' key
            }
        }
        try:
            # Send PUT request to update the row
            response = requests.put(url=update_row_url, headers=self.api_headers, json=body)
            response.raise_for_status()  # Raise exception for HTTP errors
        except requests.RequestException as e:
            # Log the error and provide debugging information
            print(f"Error updating IATA code: {e}")

    def read_cities_data(self):
        """
        Reads all city data from the Google Sheet.
        Returns:
            dict: A dictionary containing city data fetched from the sheet.
        """
        try:
            # Send GET request to fetch the data
            response = requests.get(self.deals_api_url, headers=self.api_headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()  # Return the parsed JSON data
        except requests.RequestException as e:
            # Log the error and provide debugging information
            print(f"Error fetching city data: {e}")
            return {}

    def get_customer_emails(self):
        """
        Reads all user data from the Google Sheet.
        Returns:
            list: A list containing user emails fetched from the sheet.
        """
        try:
            # Send GET request to fetch user data
            response = requests.get(self.users_api_url, headers=self.api_headers)
            response.raise_for_status()
            cust_data = response.json()
            email_list = [entry["what'sYourEmailAddress?"] for entry in cust_data["users"]]
            return email_list

        except requests.RequestException as e:
            # Log the error and provide debugging information
            print(f"Error fetching user data: {e}")
            return {}