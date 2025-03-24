from fastapi import APIRouter, HTTPException
from db.db import db_data
from models import VisaVaccinePolicy

router = APIRouter()

@router.get("/{city_name}", response_model=VisaVaccinePolicy)
async def get_policy_by_city(city_name: str):
    """
    Fetch visa and vaccine policies for a city.
    """
    countries = db_data.get("countries", {})

    for country, data in countries.items():
        if city_name.lower() in data["cities"]:
            return VisaVaccinePolicy(
                visa_policy=data["visa_policy"],
                vaccine_policy=data["vaccine_policy"]
            )

    raise HTTPException(status_code=404, detail="City not found")
