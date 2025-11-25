class Aircraft:
    def __init__(
        self,
        name: str,
        manufacturer: str,
        seats: int,
        max_range_km: int,
        speed_kmh: int,
        fuel_capacity_kg: int,
        wingspan_m: float = 0,
        length_m: float = 0,
        **extra,
    ):
        self.name = name
        self.manufacturer = manufacturer
        self.seats = seats
        self.max_range_km = max_range_km
        self.speed_kmh = speed_kmh
        self.fuel_capacity_kg = fuel_capacity_kg
        self.wingspan_m = wingspan_m
        self.length_m = length_m
        self.extra = extra

    def __repr__(self):
        return f"<Aircraft {self.name} ({self.manufacturer})>"
