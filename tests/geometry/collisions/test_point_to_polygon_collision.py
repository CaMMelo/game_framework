from gaming_framework.geometry.shape import Point2D, Polygon
from gaming_framework.geometry.collision import point_to_polygon_collision
import numpy as np
import pytest

def generate_random_polygon(n_points=6, radius=10, convexness=0, center=Point2D(0, 0)):
    points = []
    current_angle = 0
    for _ in range(n_points):
        spike = np.random.normal() * convexness * radius
        point = Point2D(
            center.x + max(0, radius + spike) * np.cos(current_angle),
            center.y + max(0, radius + spike) * np.sin(current_angle),
        )
        points.append(point)
        current_angle += 2 * np.pi / n_points
    points = sorted(points, key=lambda p: np.arctan2(p.x - center.x, p.y - center.y))
    polygon = Polygon(points)
    return polygon


@pytest.mark.parametrize("point", [
    Point2D(-10, 0),
    Point2D(-7.5, 0),
    Point2D(0, 0),
    Point2D(5, 0),
    Point2D(9.999, 0),
    Point2D(0, 8),
    Point2D(0, 6),
    Point2D(0, -4),
    Point2D(0, -8),
    Point2D(1, 1),
    Point2D(-1, 1),
    Point2D(1, -1),
    Point2D(-1, -1),
])
def test_point_is_inside_concave_polygon(point):
    polygon = generate_random_polygon()
    assert point_to_polygon_collision(point, polygon)


@pytest.mark.parametrize("point", [
    Point2D(-11, 0),
    Point2D(11, 0),
    Point2D(0, 9),
    Point2D(0, -9),
    Point2D(6, 7),
    Point2D(6, -7),
    Point2D(-6, 7),
    Point2D(-6, -7),
])
def test_point_is_outside_concave_polygon(point):
    polygon = generate_random_polygon()
    assert point_to_polygon_collision(point, polygon) == False
