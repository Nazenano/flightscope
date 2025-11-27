from api.requests import get_all_aircraft
from core.utils import latlon_to_unitvec


def fetch_airplanes():
    data = get_all_aircraft()
    planes = []
    for airplane in data["states"]:
        if airplane["latitude"] is None or airplane["longitude"] is None:
            continue

        if airplane["baro_altitude"] is not None:
            normalized_value = (airplane["baro_altitude"] - 0) / (15000 - 0)
            altitude_offset = 0.005 + (0.05 - 0.005) * normalized_value
        else:
            altitude_offset = 0.005

        planes.append(
            {
                "id": airplane["icao24"],
                "pos": latlon_to_unitvec(
                    airplane["latitude"], airplane["longitude"], height=altitude_offset
                ),
                "data": airplane,
            }
        )
    return planes
