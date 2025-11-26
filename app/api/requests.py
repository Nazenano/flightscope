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
        lamin (optional float): Minimum latitude
        lamax (optional float): Maximum latitude
        lomin (optional float): Minimum longitude
        lomax (optional float): Maximum longitude

    Returns:
        dict: JSON response from OpenSky API:
            - "time": int, UNIX timestamp of the query
            - "states": list of aircraft state vectors, where each item includes:
                - ICAO24 ID
                - Callsign
                - Latitude, Longitude, Altitude
                - Velocity, Heading, Vertical Rate
                - On-ground flag, squawk, sensors, and other live info
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

    return api.get("/states/all", params=params).json()


def get_aircraft_flights(
    icao24: str, begin: int | None = None, end: int | None = None
) -> list[dict[str, Any]]:
    """
    Retrieve historical flights for a specific aircraft.

    This returns a list of past flights for the given aircraft identified by its ICAO24 ID.
    Each flight includes departure and arrival airports, scheduled and actual times, and duration.

    Args:
        icao24 (str): ICAO24 ID of the aircraft
        begin (optional int): Unix timestamp marking the start of the query window
        end (optional int): Unix timestamp marking the end of the query window

    Returns:
        list[dict]: A list of flight records, where each record may contain:
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

    return api.get("/flights/aircraft", params=params).json()
