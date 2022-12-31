from collections import namedtuple

from gaming_framework.geometry.collision import (
    point_to_circle_collision,
    point_to_line_collision,
    point_to_point_collision,
    point_to_polygon_collision,
    point_to_rectangle_collision,
)
from gaming_framework.geometry.shape import Shape


class Point2D(namedtuple("Point2D", ["x", "y"]), Shape):
    @property
    def bounding_box(self):
        return self

    @property
    def center(self):
        return self

    def center_to(self, point):
        return point

    def point_collision(self, point):
        return point_to_point_collision(self, point)

    def line_collision(self, line):
        return point_to_line_collision(self, line)

    def circle_collision(self, circle):
        return point_to_circle_collision(self, circle)

    def rectangle_collision(self, rectangle):
        return point_to_rectangle_collision(self, rectangle)

    def polygon_collision(self, polygon):
        return point_to_polygon_collision(self, polygon)

    def collides_with(self, shape):
        return shape.point_collision(self)
