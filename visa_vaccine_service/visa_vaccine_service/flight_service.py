from fastapi import APIRouter, Query, HTTPException
import requests
import datetime

from util.constants import CITY_IATA_MAPPING, AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, TOKEN_URL, FLIGHTS_URL
 
router = APIRouter()
 
def get_access_token():
    """Fetch Amadeus API Access Token"""
    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=payload)
    return response.json().get("access_token") if response.status_code == 200 else None
 
def validate_inputs(source: str, destination: str, departure_date: str):
    """Validate source, destination, and date"""
   
    # Convert to lowercase to match dictionary keys
    source = source.lower()
    destination = destination.lower()
 
    # Check if source and destination exist in the allowed city list
    if source not in CITY_IATA_MAPPING or destination not in CITY_IATA_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid city name. Allowed cities: " + ", ".join(CITY_IATA_MAPPING.keys()))
 
    # Check if source and destination are not the same
    if source == destination:
        raise HTTPException(status_code=400, detail="Source and destination cannot be the same.")
 
    # Validate date format (YYYY-MM-DD) and check if it's in the future
    try:
        departure_date_obj = datetime.datetime.strptime(departure_date, "%Y-%m-%d").date()
        if departure_date_obj <= datetime.date.today():
            raise HTTPException(status_code=400, detail="Departure date must be in the future.")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
 
    return CITY_IATA_MAPPING[source], CITY_IATA_MAPPING[destination] # Return IATA codes
 
@router.get("/flights")
def get_flights(
    source: str = Query(..., description="City name of the source"),
    destination: str = Query(..., description="City name of the destination"),
    departure_date: str = Query(..., description="YYYY-MM-DD format"),
    adults: int = Query(1, description="Number of passengers"),
):
    """Fetch flight details from Amadeus API with input validation"""
   
    # Validate inputs and get IATA codes
    source_iata, destination_iata = validate_inputs(source, destination, departure_date)
 
    token = get_access_token()
    if not token:
        raise HTTPException(status_code=500, detail="Failed to fetch access token from Amadeus API")
 
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": source_iata,
        "destinationLocationCode": destination_iata,
        "departureDate": departure_date,
        "adults": adults,
        "currencyCode": "USD",
        "max": 5
    }
 
    response = requests.get(FLIGHTS_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
 
    return response.json()