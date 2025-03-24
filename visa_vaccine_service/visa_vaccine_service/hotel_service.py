from fastapi import FastAPI, APIRouter, Query, HTTPException
import requests
from util.constants import CITY_IATA_MAPPING, AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET, HOTEL_LIST_URL, TOKEN_URL

app = FastAPI()
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

def validate_city(city: str):
    """Validate city"""
    city = city.lower()
    if city not in CITY_IATA_MAPPING:
        raise HTTPException(status_code=400, detail="Invalid city name. Allowed cities: " + ", ".join(CITY_IATA_MAPPING.keys()))
    return CITY_IATA_MAPPING[city]  # Return IATA code

@router.get("/hotel-list")
def get_hotel_list(
    city: str = Query(..., description="City name"),
):
    """Fetch hotel list from Amadeus API"""
    city_iata = validate_city(city)

    token = get_access_token()
    if not token:
        raise HTTPException(status_code=500, detail="Failed to fetch access token from Amadeus API")

    headers = {"Authorization": f"Bearer {token}"}
    params = {"cityCode": city_iata}

    response = requests.get(HOTEL_LIST_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()

app.include_router(router)
