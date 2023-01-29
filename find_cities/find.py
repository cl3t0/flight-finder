from typing import Tuple, List
from math import cos, sin, pi, atan

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]


def get_3d_coords(point: Point2D) -> Point3D:
    lat_in_degrees, long_in_degrees = point
    lat = lat_in_degrees * pi / 180
    long = long_in_degrees * pi / 180
    return (cos(lat) * cos(long), cos(lat) * sin(long), sin(lat))


def get_average_in_3d(points: List[Point3D]) -> Point3D:
    quantity_of_points = len(points)
    return (
        sum(p[0] for p in points) / quantity_of_points,
        sum(p[1] for p in points) / quantity_of_points,
        sum(p[2] for p in points) / quantity_of_points,
    )


def projection_to_surface(point: Point3D) -> Point2D:
    x, y, z = point
    long = atan(y / x)
    lat = atan(z / (x**2 + y**2) ** (1 / 2))
    long_in_degrees = long * 180 / pi
    lat_in_degrees = lat * 180 / pi
    return (lat_in_degrees, long_in_degrees)


def get_average_coordinate(points: List[Point2D]) -> Point2D:
    points_in_3d = list(map(get_3d_coords, points))
    average_in_3d = get_average_in_3d(points_in_3d)
    average_in_surface = projection_to_surface(average_in_3d)
    return average_in_surface
