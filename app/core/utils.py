from math import radians, sin, cos, atan2, sqrt, radians
from random import uniform
from ursina.vec3 import Vec3


def haversine(lat1, lon1, lat2, lon2):
    """Calculates the great-circle distance (km) between two points using the haversine formula"""
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)

    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    return 6371 * 2 * atan2(sqrt(a), sqrt(1 - a))


def random_point():
    """Returns a random point (lat, lon)"""
    lat = uniform(-90, 90)
    lon = uniform(-180, 180)
    return lat, lon


def latlon_to_unitvec(
    lat_deg: float, lon_deg: float, radius=1.5, height=0.0, east_offset=0
):
    """Converts values :)"""
    lat_r = radians(lat_deg)
    lon_r = radians(lon_deg + 90)
    x = radius * cos(lat_r) * cos(lon_r)
    y = radius * sin(lat_r)
    z = radius * cos(lat_r) * sin(lon_r)

    surface = Vec3(x, y, z)
    normal = surface.normalized()

    east = Vec3(-sin(lon_r), 0, cos(lon_r)).normalized()
    final_pos = surface + normal * height + east * east_offset
    return final_pos
