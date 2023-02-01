import pytest
from flight_finder.mathematics import (
    get_3d_coords,
    get_average_in_3d,
    projection_to_surface,
    get_average_coordinate,
)


def test_get_3d_coords_1():
    point = (45, 45)
    result = get_3d_coords(point)
    assert result == pytest.approx((0.5, 0.5, 2 ** (-1 / 2)))


def test_get_3d_coords_2():
    point = (90, 0)
    result = get_3d_coords(point)
    assert result == pytest.approx((0, 0, 1))


def test_get_3d_coords_3():
    point = (0, -135)
    result = get_3d_coords(point)
    assert result == pytest.approx((-(2 ** (-1 / 2)), -(2 ** (-1 / 2)), 0))


def test_get_average_in_3d():
    points = [(1, 2, 3), (-3, -2, -1), (-1, -6, 4)]
    result = get_average_in_3d(points)
    assert result == (-1, -2, 2)


def test_projection_to_surface():
    point = (0.25, 0.25, 2 ** (-1 / 2) / 2)
    result = projection_to_surface(point)
    assert result == (45, 45)


def test_get_average_coordinate():
    points = [(0, 45), (0, -45), (90, 0)]
    result = get_average_coordinate(points)
    assert result == (35.264389682754654, 0)
