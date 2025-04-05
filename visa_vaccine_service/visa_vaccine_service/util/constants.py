# City to IATA code mapping
CITY_IATA_MAPPING = {
    "paris": "CDG",
    "london": "LHR",
    "new york": "JFK",
    "tokyo": "HND",
    "dubai": "DXB",
    "singapore": "SIN",
    "hong kong": "HKG",
    "bangkok": "BKK",
    "sydney": "SYD",
    "mumbai": "BOM"
}

# Amadeus API credentials
AMADEUS_CLIENT_ID = ""
    AMADEUS_CLIENT_SECRET = ""

# Amadeus API endpoints
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
HOTEL_LIST_URL = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
FLIGHTS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
