from aircraft import Aircraft

A320 = Aircraft(
    name="A320",
    manufacturer="Airbus",
    seats=180,
    max_range_km=6100,
    speed_kmh=840,
    fuel_capacity_kg=24210,
    wingspan_m=35.8,
    length_m=37.6,
)

B737 = Aircraft(
    name="Boeing 737-800",
    manufacturer="Boeing",
    seats=189,
    max_range_km=5436,
    speed_kmh=842,
    fuel_capacity_kg=26020,
    wingspan_m=35.8,
    length_m=39.5,
)

E190 = Aircraft(
    name="Embraer E190",
    manufacturer="Embraer",
    seats=100,
    max_range_km=4500,
    speed_kmh=829,
    fuel_capacity_kg=12970,
)

ALL_AIRCRAFT = [A320, B737, E190]
