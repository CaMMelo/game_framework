from gaming_framework.geometry.collision import point_to_line_collision
from gaming_framework.geometry.shape import Line2D, Point2D


def test_point_is_colliding_with_line():
    point = Point2D(0, 0)
    line = Line2D(Point2D(-1, -1), Point2D(1, 1))
    assert point_to_line_collision(point, line)


def test_point_is_above_line():
    point = Point2D(-1, 1)
    line = Line2D(Point2D(-1, -1), Point2D(1, 1))
    assert point_to_line_collision(point, line) == False


def test_point_is_bellow_line():
    point = Point2D(1, -1)
    line = Line2D(Point2D(-1, -1), Point2D(1, 1))
    assert point_to_line_collision(point, line) == False
