from fastapi import APIRouter, HTTPException, Query
from services.car_rental_service import get_available_cars

router = APIRouter()

@router.get("/")
def fetch_cars(location: str = Query(..., description="Pickup location")):
    """
    API endpoint to fetch available cars by location.
    """
    cars = get_available_cars(location)

    if not cars:
        raise HTTPException(status_code=404, detail="No available cars found at this location.")

    return {"available_cars": cars}
