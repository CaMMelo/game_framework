from collections import namedtuple
from dataclasses import dataclass, field

import numpy as np

from gaming_framework.geometry.collision import (
    circle_to_circle_collision,
    circle_to_polygon_collision,
    circle_to_rectangle_collision,
    line_to_circle_collision,
    line_to_line_collision,
    line_to_polygon_collision,
    line_to_rectangle_collision,
    point_to_circle_collision,
    point_to_line_collision,
    point_to_point_collision,
    point_to_polygon_collision,
    point_to_rectangle_collision,
    polygon_to_polygon_collision,
    rectangle_to_polygon_collision,
    rectangle_to_rectangle_collision,
)


class Shape:
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def bounding_box(self):
        raise NotImplementedError()

    def center_to(self, point):
        raise NotImplementedError()

    def point_collision(self, point):
        raise NotImplementedError()

    def line_collision(self, line):
        raise NotImplementedError()

    def circle_collision(self, circle):
        raise NotImplementedError()

    def rectangle_collision(self, rectangle):
        raise NotImplementedError()

    def polygon_collision(self, polygon):
        raise NotImplementedError()

    def collides_with(self, shape):
        raise NotImplementedError()


class Point2D(namedtuple("Point2D", ["x", "y"]), Shape):
    def __add__(self, other):
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point2D(self.x - other.x, self.y - other.y)

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

    def distance(self, other):
        return np.linalg.norm(np.array(self - other))

    def scalar_mult(self, scalar):
        return Point2D(self.x * scalar, self.y * scalar)

    def scalar_div(self, scalar):
        return self.scalar_mult(1 / scalar)


class Line2D(namedtuple("Line2D", ["a", "b"]), Shape):
    _center: Point2D = field(init=False, default=None)
    _size: float = field(init=False, default=0)
    _bouding_box: "Circle" = field(init=False, default=None)

    @property
    def bounding_box(self):
        if self._bouding_box is not None:
            return self._bouding_box
        radius = self.size / 2
        self._bouding_box = Circle(self.center, radius)
        return self._bouding_box

    @property
    def center(self):
        if self._center is not None:
            return self._center
        c = self.a + self.b
        self._center = Point2D(c.x / 2, c.y / 2)
        return self._center

    @property
    def size(self):
        if self._size is not None:
            return self._size
        self._size = self.a.distance(self.b)

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


@dataclass
class Circle(Shape):
    center: Point2D
    radius: float

    @property
    def bounding_box(self):
        return self

    def center_to(self, point):
        return Circle(point, self.radius)

    def point_collision(self, point):
        return point_to_circle_collision(point, self)

    def line_collision(self, line):
        return line_to_circle_collision(line, self)

    def circle_collision(self, circle):
        return circle_to_circle_collision(self, circle)

    def rectangle_collision(self, rectangle):
        return circle_to_rectangle_collision(self, rectangle)

    def polygon_collision(self, polygon):
        return circle_to_polygon_collision(self, polygon)

    def collides_with(self, shape):
        return shape.circle_collision(self)


@dataclass
class Rectangle(Shape):
    top_left: Point2D
    bottom_right: Point2D
    _center: Point2D = field(init=False, default=None)
    _lines: list[Line2D] = field(init=False, default=None)
    _points: list[Point2D] = field(init=False, default=None)
    _bounding_box: Circle = field(init=False, default=None)

    @property
    def bounding_box(self):
        if self._bounding_box is not None:
            return self._bounding_box
        radius = self.top_left.distance(self.bottom_right) / 2
        self._bounding_box = Circle(self.center, radius)
        return self._bounding_box

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
        c = self.top_left + self.bottom_right
        self._center = Point2D(c.x / 2, c.y / 2)
        return self._center

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


@dataclass
class Polygon(Shape):
    points: list[Point2D]
    _center: Point2D = field(init=False, default=None)
    _bounding_box: Circle = field(init=False, default=None)
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
        c = top_left + bottom_right
        center = Point2D(c.x / 2, c.y / 2)
        radius = top_left.distance(bottom_right) / 2
        self._bounding_box = Circle(center, radius)
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
