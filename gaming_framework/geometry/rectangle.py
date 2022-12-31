from dataclasses import dataclass, field

from gaming_framework.geometry.collision import (
    circle_to_rectangle_collision,
    line_to_rectangle_collision,
    point_to_rectangle_collision,
    rectangle_to_polygon_collision,
    rectangle_to_rectangle_collision,
)
from gaming_framework.geometry.line import Line2D
from gaming_framework.geometry.point import Point2D
from gaming_framework.geometry.shape import Shape


@dataclass
class Rectangle(Shape):
    top_left: Point2D
    bottom_right: Point2D
    _center: Point2D = field(init=False, default=None)
    _lines: list[Line2D] = field(init=False, default=None)
    _points: list[Point2D] = field(init=False, default=None)

    @property
    def bounding_box(self):
        return self

    @property
    def points(self):
        if self._points is not None:
            return self._points
        self._points = [
            self.top_left,
            Point2D(self.bottom_right.x, self.top_left.y),
            self.bottom_right,
            Point2D(self.top_left.x, self.bottom_right.y),
        ]
        return self._points

    @property
    def lines(self):
        if self._lines is not None:
            return self._lines
        self._lines = []
        for i, pa in enumerate(self.points):
            pb = self.points[(i + 1) % len(self.points)]
            self._lines.append(Line2D(pa, pb))
        return self._lines

    @property
    def center(self):
        if self._center is not None:
            return self._center
        cx = (self.top_left.x + self.bottom_right.x) / 2
        cy = (self.top_left.y + self.bottom_right.y) / 2
        self._center = Point2D(cx, cy)

    def center_to(self, point):
        dx = point.x - self.center.x
        dy = point.y - self.center.y
        top = self.top_left.y + dy
        left = self.top_left.x + dx
        bottom = self.bottom_right.y + dy
        right = self.bottom_right.x + dx
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        return Rectangle(top_left, bottom_right)

    def point_collision(self, point):
        return point_to_rectangle_collision(point, self)

    def line_collision(self, line):
        return line_to_rectangle_collision(line, self)

    def circle_collision(self, circle):
        return circle_to_rectangle_collision(circle, self)

    def rectangle_collision(self, rectangle):
        return rectangle_to_rectangle_collision(self, rectangle)

    def polygon_collision(self, polygon):
        return rectangle_to_polygon_collision(self, polygon)

    def collides_with(self, shape):
        return shape.rectangle_collision(self)
