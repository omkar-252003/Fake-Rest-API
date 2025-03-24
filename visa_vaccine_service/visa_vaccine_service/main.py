from fastapi import FastAPI
from routes import visa_vaccine, car_rental

from hotel_service import router as hotel_router
from flight_service import router as flight_router

app = FastAPI(title=" AGENT MAX : Travel Services API ")

# Include routers

app.include_router(flight_router, prefix="/api/flight", tags=["Flight Services"])
app.include_router(visa_vaccine.router, prefix="/api/policy", tags=["Visa & Vaccine"])
app.include_router(hotel_router, prefix="/api/hotels", tags=["Hotel Services"])
app.include_router(car_rental.router, prefix="/api/cars", tags=["Car Rental"])

@app.get("/")
async def root():
    return {"message": "Welcome to Travel Services API"}
