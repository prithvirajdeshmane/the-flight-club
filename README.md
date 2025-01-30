# Flight Deals Finder

This project is a flight deals notification program. It fetches flight data from the Amadeus API, compares prices with user-defined thresholds, and sends notifications via WhatsApp using Twilio if a cheaper flight is available. Additionally, it manages destination city data using Google Sheets (via the Sheety API).

---

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup and Installation](#setup-and-installation)
4. [Environment Variables](#environment-variables)
5. [File Overview](#file-overview)
6. [Usage](#usage)
7. [Future Enhancements](#future-enhancements)

---

## Features

- Fetches city IATA codes and flight offers using Amadeus API.
- Stores destination data in a Google Sheet and keeps it updated.
- Reads a list of emails of users subscribed to the service
- Compares current flight prices to pre-defined thresholds.
- Sends Email notifications via SMTP to all user emails about deals below the threshold price.

---

## Technologies Used

- **Python**: Programming language.
- **smtplib**: Sends email notifications.
- **Amadeus API**: Fetches flight and city data.
- **Sheety API**: Manages destination and user data stored in Google Sheets.

---

## Setup and Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/the-flight-club.git
    cd the-flight-club
    ```

2. Install dependencies:

3. Create a Google Sheet for storing flight data, and connect it to the Sheety API.

4. Configure API keys and tokens as environment variables (see [Environment Variables](#environment-variables)).

5. Run the program:
    ```bash
    python main.py
    ```

---

## Environment Variables

The program relies on several environment variables to connect with external services:

- **Amadeus API**:
  - `AMADEUS_FLIGHTSEARCH_API_KEY`: Amadeus API client ID.
  - `AMADEUS_FLIGHTSEARCH_API_SECRET`: Amadeus API client secret.

- **SMTP (These are for Gmail setup, if using Yahoo or another client, please configure as needed**:
  - `GMAIL_TEST_EMAIL`: Sender Gmail address for sending notifications from
  - `GMAIL_TEST_APP_PWD`: App Password setup in Gmail for SMTP.
  - `GMAIL_SMTP_PORT`: 587
  - `GMAIL_SMTP`: SMTP address for Google.

- **Sheety API**:
  - `SHEETY_FLIGHTDEALS_URL`: URL of the Sheety API endpoint.
  - `SHEETY_BEARER_TOKEN`: Bearer token for Sheety API authentication.

---

## File Overview

### 1. `main.py`
- The entry point of the program. It:
  - Reads destination data from Google Sheets.
  - Reads user emails from Google Sheets.
  - Ensures all destination cities have IATA codes.
  - Searches for flights for each destination.
    - First searches non-stop flights
    - If none found, then searches for flights with layovers
  - Sends email notifications to each user for flights below the threshold price.

### 2. `flight_search.py`
- Handles API calls to the Amadeus API to:
  - Fetch city IATA codes.
  - Search for flight offers.

### 3. `flight_data.py`
- Processes flight data and identifies the cheapest flight.

### 4. `notification_manager.py`
- Sends email notiications to each email in list using SMTP.

### 5. `data_manager.py`
- Handles interaction with Google Sheets via the Sheety API.

---

## Usage

1. **Configure Google Sheet**:
   - Add columns names in order: `id`, `city`, `iataCode`, and `lowestPrice`.
   - Populate the `city` and `lowestPrice` columns for each destination, where the lowest price is the user threshold.

2. **Create Form for Users**:
   - Create form, with 3 required questions
     - "What's your first name?"
     - "What's your last name?"
     - "What's your email?"
   - Link the form to the destinations Google Sheet created in Step 1
   - Copy form link, open link in another browser, answer questions to add data to form
     - Alternatively, fill in form with some test user emails
   - NOTE: For emails, enter an email address where you can receive and check the notification emails sent

3. **Run the Program**:
   - Execute `main.py` to fetch flight data, update the Google Sheet, and send notifications for deals.

4. **View Notifications**:
   - Check your recipient email addresses for messages about flight deals.

---

## Future Enhancements

- Implement retries and error recovery for API calls.
- Allow configuration of flight search parameters (e.g., currency, number of passengers) via a UI or configuration file.
- Add support for bulk updates to the Google Sheet for faster data handling.
- Enhance logging and monitoring.

---
## License
This project is licensed under the [GNU General Public Use v3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

---
## Affiliation
This code is part of the Udemy course "100 Days of Code: The Complete Python Pro Bootcamp" by Dr. Angela Yu and AppBrewery.

---
## Acknowledgments

- [Amadeus API](https://developers.amadeus.com/) for flight and city data.
- [Sheety API](https://sheety.co/) for managing Google Sheets.

---
## Author
Prithviraj Deshmane
