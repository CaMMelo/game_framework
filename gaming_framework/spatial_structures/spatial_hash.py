from dataclasses import dataclass, field

from gaming_framework.geometry.shape import (
    Circle,
    Point2D,
    Rectangle,
    Shape,
    ShapeVisitor,
)
from gaming_framework.spatial_structures.spatial_object import SpatialObject
from gaming_framework.spatial_structures.spatial_structure import SpatialStructure


@dataclass
class ShapeHash(ShapeVisitor):
    bounds: Rectangle
    number_of_rows: int
    number_of_lines: int

    def accept_point(self, point: Point2D) -> tuple[int, int]:
        x = int(
            abs(point.x - self.bounds.top_left.x)
            // (self.bounds.width / self.number_of_rows)
        )
        y = int(
            abs(point.y - self.bounds.top_left.y)
            // (self.bounds.height / self.number_of_lines)
        )
        if point.x < self.bounds.top_left.x:
            x = -x
        if point.y > self.bounds.top_left.y:
            y = -y
        return (x, y)

    def accept_circle(self, circle: Circle) -> list[tuple[int, int]]:
        top_left = self.accept_point(
            Point2D(circle.center.x - circle.radius, circle.center.y + circle.radius)
        )
        bottom_right = self.accept_point(
            Point2D(circle.center.x + circle.radius, circle.center.y - circle.radius)
        )
        points = []
        if top_left and bottom_right:
            points.extend(
                (row, col)
                for row in range(top_left[0], bottom_right[0] + 1)
                for col in range(top_left[1], bottom_right[1] + 1)
                if (row, col) not in points
            )
        return points

    def accept_rectangle(self, rectangle: Rectangle) -> list[tuple[int, int]]:
        top_left = self.accept_point(rectangle.top_left)
        bottom_right = self.accept_point(rectangle.bottom_right)
        points = []
        if top_left and bottom_right:
            points.extend(
                (row, col)
                for row in range(top_left[0], bottom_right[0] + 1)
                for col in range(top_left[1], bottom_right[1] + 1)
                if (row, col) not in points
            )
        return points


@dataclass
class SpatialHash(SpatialStructure):
    bounds: Rectangle
    number_of_rows: int = 20
    number_of_lines: int = 20
    _map: dict[tuple[int, int], list[SpatialObject]] = field(
        init=False, default_factory=dict
    )
    _hash_visitor: ShapeHash = field(init=False)

    def __post_init__(self):
        self._hash_visitor = ShapeHash(
            self.bounds, self.number_of_rows, self.number_of_lines
        )

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def __insert_into(self, object: SpatialObject, hashes: list[tuple[int, int]]):
        for hash in hashes:
            if hash not in self._map:
                self._map[hash] = []
            if object not in self._map[hash]:
                self._map[hash].append(object)

    def insert(self, object: SpatialObject):
        hashes = self._hash_visitor.visit(object.bounding_box)
        self.__insert_into(object, hashes)

    def remove(self, object: SpatialObject):
        removed = False
        for objects in self._map.values():
            if object in objects:
                objects.remove(object)
                removed = True
        if removed:
            object.unsubscribe(self)

    def get_objects(self) -> list[SpatialObject]:
        objects = []
        objects.extend(
            object
            for cell in self._map.values()
            for object in cell
            if object not in objects
        )
        yield from objects

    def query(self, shape: Shape) -> list[SpatialObject]:
        hashes = self._hash_visitor.visit(shape)
        yield from (
            object for hash in hashes if hash in self._map for object in self._map[hash]
        )

    def empty_copy(self) -> "SpatialHash":
        return SpatialHash(
            bounds=self.bounds,
            number_of_rows=self.number_of_rows,
            number_of_lines=self.number_of_lines,
        )
