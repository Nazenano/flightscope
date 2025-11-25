from typing import List
from app.core.utils import random_point, haversine
from app.simulation.flight import Flight
from app.simulation.aircraft_models import random_aircraft_model
import random


def generate_flights(n: int) -> List[Flight]:
    """Generate a list of n Flight objects with random parameters"""

    flights: List[Flight] = []

    for i in range(n):
        aircraft_name, data = random_aircraft_model()

        lat1, lon1 = random_point()

        destination = None
        while True:
            lat2, lon2 = random_point()
            distance = haversine(lat1, lon1, lat2, lon2)
            if distance <= data["range_km"]:
                destination = (lat2, lon2)
                break

        flight_id = f"FL{i+1:03d}"
        altitude_ft = data["cruise_altitude_ft"]
        speed_kn = data["cruise_speed_kn"]
        progress = round(random.uniform(0, 1), 2)

        flight = Flight(
            flight_id=flight_id,
            aircraft=aircraft_name,
            origin=(lat1, lon1),
            destination=destination,
            altitude_ft=altitude_ft,
            speed_kn=speed_kn,
            progress=progress,
        )

        flights.append(flight)

    return flights
