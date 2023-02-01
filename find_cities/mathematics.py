from typing import Tuple, List
from math import cos, sin, pi, atan

Point2D = Tuple[float, float]
Point3D = Tuple[float, float, float]


def get_3d_coords(point: Point2D) -> Point3D:
    """
    Given a point in 2D coordinates, returns the point in 3D coordinates.

    :param point: Tuple of latitude and longitude in degrees
    :return: Tuple of x, y, and z in 3D coordinates
    """
    lat_in_degrees, long_in_degrees = point
    lat = lat_in_degrees * pi / 180
    long = long_in_degrees * pi / 180
    return (cos(lat) * cos(long), cos(lat) * sin(long), sin(lat))


def get_average_in_3d(points: List[Point3D]) -> Point3D:
    """
    Given a list of points in 3D coordinates, returns the average of the points.

    :param points: List of points in 3D coordinates
    :return: Tuple of x, y, and z of the average point in 3D coordinates
    """
    quantity_of_points = len(points)
    return (
        sum(p[0] for p in points) / quantity_of_points,
        sum(p[1] for p in points) / quantity_of_points,
        sum(p[2] for p in points) / quantity_of_points,
    )


def projection_to_surface(point: Point3D) -> Point2D:
    """
    Given a point in 3D coordinates, returns the projection of the point onto the surface.

    :param point: Tuple of x, y, and z in 3D coordinates
    :return: Tuple of latitude and longitude in degrees
    """
    x, y, z = point
    long = atan(y / x)
    lat = atan(z / (x**2 + y**2) ** (1 / 2))
    long_in_degrees = long * 180 / pi
    lat_in_degrees = lat * 180 / pi
    return (lat_in_degrees, long_in_degrees)


def get_average_coordinate(points: List[Point2D]) -> Point2D:
    """
    Given a list of points in 2D coordinates, returns the average of the points.

    :param points: List of points in 2D coordinates
    :return: Tuple of latitude and longitude of the average point in degrees
    """
    points_in_3d = list(map(get_3d_coords, points))
    average_in_3d = get_average_in_3d(points_in_3d)
    average_in_surface = projection_to_surface(average_in_3d)
    return average_in_surface
