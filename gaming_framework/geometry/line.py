from collections import namedtuple
from dataclasses import field

from gaming_framework.geometry.collision import (
    line_to_circle_collision,
    line_to_line_collision,
    line_to_polygon_collision,
    line_to_rectangle_collision,
    point_to_line_collision,
)
from gaming_framework.geometry.point import Point2D
from gaming_framework.geometry.shape import Shape


class Line2D(namedtuple("Line2D", ["a", "b"]), Shape):
    _center: Point2D = field(init=False, default=None)

    @property
    def bounding_box(self):
        return self

    @property
    def center(self):
        if self._center is not None:
            return self._center
        cx = (self.b.x + self.a.x) / 2
        cy = (self.b.y + self.a.y) / 2
        self._center = Point2D(cx, cy)
        return self._center

    def center_to(self, point):
        dx = point.x - self.center.x
        dy = point.y - self.center.y
        a = Point2D(self.a.x + dx, self.a.y + dy)
        b = Point2D(self.b.x + dx, self.b.y + dy)
        return Line2D(a, b)

    def point_collision(self, point):
        return point_to_line_collision(self, point)

    def line_collision(self, line):
        return line_to_line_collision(self, line)

    def circle_collision(self, circle):
        return line_to_circle_collision(self, circle)

    def rectangle_collision(self, rectangle):
        return line_to_rectangle_collision(self, rectangle)

    def polygon_collision(self, polygon):
        return line_to_polygon_collision(self, polygon)

    def collides_with(self, shape):
        return shape.line_collision(self)
