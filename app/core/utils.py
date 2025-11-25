import math
import random


def haversine(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance (km) between two points using the haversine formula"""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def random_point():
    """Returns a random point (lat, lon)"""
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    return lat, lon
