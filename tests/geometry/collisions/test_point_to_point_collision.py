from gaming_framework.geometry.collision import point_to_point_collision
from gaming_framework.geometry.shape import Point2D
from random import randint


def test_equal_points_collides():
    x, y = randint(0, 100), randint(0, 100)
    point_a = Point2D(x, y)
    point_b = Point2D(x, y)

    assert point_to_point_collision(point_a, point_b)


def test_different_points_do_not_collide():
    x, y = randint(0, 100), randint(0, 100)
    point_a = Point2D(0, 0)
    x, y = x + randint(-100, 100), y + randint(-100, 100)
    point_b = Point2D(0, 1)

    assert point_to_point_collision(point_a, point_b) == False
