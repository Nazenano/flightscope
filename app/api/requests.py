from typing import Any
from .client import APIClient

api = APIClient()


def get_all_aircraft(
    lamin: float | None = None,
    lamax: float | None = None,
    lomin: float | None = None,
    lomax: float | None = None,
) -> dict[str, Any]:
    """
    Get all current aircraft in the air.

    Optionally filter by bounding box.

    Args:
        - lamin (optional float): Minimum latitude
        - lamax (optional float): Maximum latitude
        - lomin (optional float): Minimum longitude
        - lomax (optional float): Maximum longitude

    Returns: dict
        - time (int): Unix timestamp when the data snapshot was generated.
        - states (list[dict]): List of aircraft state dictionaries. Each aircraft contains:
            - icao24 (str): Unique 24-bit ICAO aircraft identifier.
            - callsign (str or None): Aircraft callsign if available.
            - origin_country (str): Country of registration.
            - time_position (int or None): Timestamp of last position update.
            - last_contact (int): Timestamp of last received message.
            - longitude (float or None): Aircraft longitude in degrees.
            - latitude (float or None): Aircraft latitude in degrees.
            - baro_altitude (float or None): Barometric altitude in meters.
            - on_ground (bool): True if the aircraft is on the ground.
            - velocity (float or None): Ground speed in meters per second.
            - heading (float or None): Direction of travel in degrees (0–360).
            - vertical_rate (float or None): Climb or descent rate in meters per second.
            - sensors (list[int] or None): Sensor IDs contributing position data.
            - geo_altitude (float or None): Geometric altitude in meters.
            - squawk (str or None): Assigned transponder squawk code.
            - spi (bool): Special Position Identification flag.
            - position_source (int): Source of position data (0=ADS-B, 1=ASTERIX, 2=MLAT).
    """
    params: dict[str, float] = {}

    if lamin is not None:
        params["lamin"] = lamin
    if lamax is not None:
        params["lamax"] = lamax
    if lomin is not None:
        params["lomin"] = lomin
    if lomax is not None:
        params["lomax"] = lomax

    response = api.get("/states/all", params=params)
    raw = None
    try:
        raw = response.json()
    except:
        print("Error:", response.text)
        return {}

    parsed_states = []
    for s in raw.get("states", []):
        parsed_states.append(
            {
                "icao24": s[0],
                "callsign": s[1],
                "origin_country": s[2],
                "time_position": s[3],
                "last_contact": s[4],
                "longitude": s[5],
                "latitude": s[6],
                "baro_altitude": s[7],
                "on_ground": s[8],
                "velocity": s[9],
                "heading": s[10],
                "vertical_rate": s[11],
                "sensors": s[12],
                "geo_altitude": s[13],
                "squawk": s[14],
                "spi": s[15],
                "position_source": s[16],
            }
        )

    return {
        "time": raw.get("time"),
        "states": parsed_states,
    }


def get_aircraft_flights(
    icao24: str, begin: int | None = None, end: int | None = None
) -> list[dict[str, Any]]:
    """
    Retrieve historical flights for a specific aircraft.

    This returns a list of past flights for the given aircraft identified by its ICAO24 ID.
    Each flight includes departure and arrival airports, scheduled and actual times, and duration.

    Args:
        - icao24 (str): ICAO24 ID of the aircraft
        - begin (optional int): Unix timestamp marking the start of the query window
        - end (optional int): Unix timestamp marking the end of the query window

    Returns: list[dict]: A list of flight records, where each record may contain:
            - "icao24": str, aircraft ID
            - "estDepartureAirport": str, departure airport ICAO code
            - "estArrivalAirport": str, arrival airport ICAO code
            - "firstSeen": int, timestamp of takeoff
            - "lastSeen": int, timestamp of landing
            - "callsign": str, flight callsign
            - Additional flight metadata depending on OpenSky API response
    """
    params: dict[str, int | str] = {"icao24": icao24}

    if begin is not None:
        params["begin"] = begin
    if end is not None:
        params["end"] = end

    response = api.get("/flights/aircraft", params=params)
    try:
        return response.json()
    except:
        print("Error:", response.text)
        return []


def get_aircraft_metadata(icao24: str) -> dict[str, Any]:
    """
    Fetch detailed metadata for a specific aircraft from OpenSky.

    Args:
        - icao24 (str): ICAO 24-bit identifier of the aircraft.

    Returns: dict with keys:
        - icao24 (str)
        - registration (str or None)
        - manufacturer (str or None)
        - model (str or None)
        - typecode (str or None)
        - serial_number (str or None)
    """
    if not icao24 or len(icao24) != 6:
        print(f"Invalid icao24: {icao24}")
        return {}

    response = api.get(f"/metadata/aircraft/icao/{icao24}")
    raw = None

    try:
        raw = response.json()
    except Exception:
        print("Error parsing metadata:", response.text)
        return {}

    return {
        "icao24": raw.get("icao24", icao24),
        "registration": raw.get("registration"),
        "manufacturer": raw.get("manufacturericao") or raw.get("manufacturername"),
        "model": raw.get("model"),
        "typecode": raw.get("typecode"),
        "serial_number": raw.get("serialnumber") or raw.get("serial_number"),
    }

