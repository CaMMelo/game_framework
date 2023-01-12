from gaming_framework.geometry.shape import Point2D, Polygon
from gaming_framework.geometry.collision import point_to_polygon_collision
import numpy as np


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


def test_point_is_inside_concave_polygon():
    polygon = generate_random_polygon()
    point = Point2D(-20, 0)
    assert point_to_polygon_collision(point, polygon)


# def test_point_is_leftside_concave_polygon():
#     polygon = generate_random_polygon()
#     point = (-11, 0)
#     assert point_to_polygon_collision(point, polygon) == False

# def test_point_is_rightside_concave_polygon():
#     polygon = generate_random_polygon()
#     point = (20, 0)
#     assert point_to_polygon_collision(point, polygon) == False