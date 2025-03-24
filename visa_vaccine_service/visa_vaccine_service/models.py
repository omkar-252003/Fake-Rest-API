from pydantic import BaseModel
from typing import Optional, Dict

class VisaVaccinePolicy(BaseModel):
    visa_policy: str
    vaccine_policy: str

class Car(BaseModel):
    car_id: int
    brand: str
    model: str
    seat_capacity: int
    location: str
    price_per_day: int
    available: bool
