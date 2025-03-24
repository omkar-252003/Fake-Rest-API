from db.db import db_data

def get_available_cars(location: str):
    """Fetch available cars based on location."""
    car_types = db_data.get("car_types", [])
    available_cars = []

    for category in car_types:
        for car in category["cars"]:
            if car["location"].lower() == location.lower() and car["available"]:
                available_cars.append(car)

    return available_cars
