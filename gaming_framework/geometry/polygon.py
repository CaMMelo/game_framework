from dataclasses import dataclass, field

from gaming_framework.geometry.collision import (
    circle_to_polygon_collision,
    line_to_polygon_collision,
    point_to_polygon_collision,
    polygon_to_polygon_collision,
    rectangle_to_polygon_collision,
)
from gaming_framework.geometry.line import Line2D
from gaming_framework.geometry.point import Point2D
from gaming_framework.geometry.rectangle import Rectangle
from gaming_framework.geometry.shape import Shape


@dataclass
class Polygon(Shape):
    points: list[Point2D]
    _center: Point2D = field(init=False, default=None)
    _bounding_box: Rectangle = field(init=False, default=None)
    _lines: list[Line2D] = field(init=False, default=None)

    @property
    def bounding_box(self):
        if self._bounding_box is not None:
            return self._bounding_box
        top = max(point.y for point in self.points)
        left = min(point.x for point in self.points)
        bottom = min(point.y for point in self.points)
        right = max(point.x for point in self.points)
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        self._bounding_box = Rectangle(top_left, bottom_right)
        return self._bounding_box

    @property
    def center(self):
        if self._center is not None:
            return self._center
        self._center = self.bounding_box.center
        return self._center

    @property
    def lines(self):
        if self._lines is not None:
            return self._lines
        self._lines = []
        for i, point_a in enumerate(self.points):
            point_b = self.points[(i + 1) % len(self.points)]
            self._lines.append(Line2D(point_a, point_b))
        return self._lines

    def center_to(self, point):
        dx = point.x - self.center.x
        dy = point.y - self.center.y
        return Polygon([Point2D(p.x + dx, p.y + dy) for p in self.polygon.points])

    def point_collision(self, point):
        return point_to_polygon_collision(point, self)

    def line_collision(self, line):
        return line_to_polygon_collision(line, self)

    def circle_collision(self, circle):
        return circle_to_polygon_collision(circle, self)

    def rectangle_collision(self, rectangle):
        return rectangle_to_polygon_collision(rectangle, self)

    def polygon_collision(self, polygon):
        return polygon_to_polygon_collision(self, polygon)

    def collides_with(self, shape):
        return shape.polygon_collision(self)
