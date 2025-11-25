import math
from typing import Optional, Tuple


class Flight:
    def __init__(
        self,
        flight_id: str,
        aircraft: str,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        altitude_ft: float,
        speed_kn: float,
        progress: Optional[float] = None,
    ):
        self.flight_id = flight_id
        self.aircraft = aircraft
        self.origin = origin
        self.destination = destination
        self.altitude_ft = altitude_ft
        self.speed_kn = speed_kn
        self.heading = self._calculate_heading()
        self.progress = progress if progress is not None else 0.0

    def _calculate_heading(self) -> float:
        """Compute the bearing from origin to destination"""
        lat1, lon1 = map(math.radians, self.origin)
        lat2, lon2 = map(math.radians, self.destination)
        dlon = lon2 - lon1
        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(
            lat2
        ) * math.cos(dlon)
        heading = math.degrees(math.atan2(x, y))
        return (heading + 360) % 360

    def current_position(self) -> Tuple[float, float]:
        """Returns current lat/lon along route based on progress"""
        lat1, lon1 = self.origin
        lat2, lon2 = self.destination
        lat = lat1 + (lat2 - lat1) * self.progress
        lon = lon1 + (lon2 - lon1) * self.progress
        return lat, lon

    def to_dict(self) -> dict:
        return {
            "id": self.flight_id,
            "aircraft": self.aircraft,
            "origin": self.origin,
            "destination": self.destination,
            "altitude_ft": self.altitude_ft,
            "speed_kts": self.speed_kn,
            "heading": self.heading,
            "progress": self.progress,
        }

    def __repr__(self):
        return f"<Flight {self.flight_id}: {self.aircraft} from {self.origin} → {self.destination} @ {self.altitude_ft} ft at {int(self.progress * 100)}%>"


