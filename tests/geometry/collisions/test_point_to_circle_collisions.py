import numpy as np

from gaming_framework.geometry.collision import point_to_circle_collision
from gaming_framework.geometry.shape import Circle, Point2D


def test_point_is_inside_circle():
    point = Point2D(1, 1)
    circle = Circle(Point2D(0, 0), 5)
    assert point_to_circle_collision(point, circle)


def test_point_is_outside_circle():
    point = Point2D(6, 1)
    circle = Circle(Point2D(0, 0), 5)
    assert point_to_circle_collision(point, circle) == False


def test_point_is_on_circles_edge():
    point = (2, 3)
    norm = (point / np.linalg.norm(point)) * 5
    point = Point2D(norm[0], norm[1])
    circle = Circle(Point2D(0, 0), 5)
    assert point_to_circle_collision(point, circle)
