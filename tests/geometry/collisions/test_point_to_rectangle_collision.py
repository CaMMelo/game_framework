from gaming_framework.geometry.collision import point_to_rectangle_collision
from gaming_framework.geometry.shape import Point2D, Rectangle


def test_point_is_inside_rectangle():
    point = Point2D(0, 0)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_is_outside_on_top_of_rectangle():
    point = Point2D(0, 2)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle) == False


def test_point_is_outside_on_right_of_rectangle():
    point = Point2D(2, 0)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle) == False


def test_point_is_outside_on_bottom_of_rectangle():
    point = Point2D(0, -2)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle) == False


def test_point_is_outside_on_left_of_rectangle():
    point = Point2D(-2, 0)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle) == False


def test_point_is_on_top_edge_of_rectangle():
    point = Point2D(0, 1)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_is_on_right_edge_of_rectangle():
    point = Point2D(1, 0)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_is_on_bottom_edge_of_rectangle():
    point = Point2D(0, -1)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_is_on_left_edge_of_rectangle():
    point = Point2D(-1, 0)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_in_on_top_left_edge_of_rectangle():
    point = Point2D(-1, 1)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_in_on_top_right_edge_of_rectangle():
    point = Point2D(1, 1)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_in_on_bottom_right_edge_of_rectangle():
    point = Point2D(1, -1)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)


def test_point_in_on_bottom_left_edge_of_rectangle():
    point = Point2D(-1, -1)
    rectangle = Rectangle(Point2D(-1, 1), Point2D(1, -1))
    assert point_to_rectangle_collision(point, rectangle)
