from dataclasses import dataclass, field

from gaming_framework.geometry.collision import (
    circle_to_circle_collision,
    circle_to_polygon_collision,
    circle_to_rectangle_collision,
    line_to_circle_collision,
    point_to_circle_collision,
)
from gaming_framework.geometry.point import Point2D
from gaming_framework.geometry.rectangle import Rectangle
from gaming_framework.geometry.shape import Shape


@dataclass
class Circle(Shape):
    center: Point2D
    radius: float
    _bounding_box: Rectangle = field(init=False, default=None)

    @property
    def bounding_box(self):
        if self._bounding_box is not None:
            return self._bounding_box
        top = self.center.y + self.radius
        left = self.center.x - self.radius
        bottom = self.center.y - self.radius
        right = self.center.x + self.radius
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        self._bounding_box = Rectangle(top_left, bottom_right)
        return self._bounding_box

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
