from dataclasses import dataclass, field

from gaming_framework.geometry.shape import Point2D, Rectangle, Shape
from gaming_framework.spatial_structures.spatial_object import SpatialObject
from gaming_framework.spatial_structures.spatial_structure import SpatialStructure


@dataclass
class QuadTree(SpatialStructure):
    bounds: Rectangle
    max_objects: int = 4
    depth: int = 0
    max_depth: int = 10
    objects: list[SpatialObject] = field(default_factory=list)
    children: list["QuadTree"] = field(default_factory=list)

    _all_objects: list[SpatialObject] = field(init=False, default_factory=list)

    def __post_init__(self):
        for object in self.objects:
            self.insert(object)

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other) -> bool:
        return id(self) == id(other)

    def __divide(self):
        if self.depth > self.max_depth:
            return
        mid_x = (self.bounds.top_left.x + self.bounds.bottom_right.x) / 2
        mid_y = (self.bounds.top_left.y + self.bounds.bottom_right.y) / 2

        top_mid_point = Point2D(mid_x, self.bounds.top_left.y)
        right_mid_point = Point2D(self.bounds.bottom_right.x, mid_y)
        mid_point = Point2D(mid_x, mid_y)
        bottom_mid_point = Point2D(mid_x, self.bounds.bottom_right.y)
        left_mid_point = Point2D(self.bounds.top_left.x, mid_y)

        child_bounds = [
            Rectangle(self.bounds.top_left, mid_point),
            Rectangle(top_mid_point, right_mid_point),
            Rectangle(mid_point, self.bounds.bottom_right),
            Rectangle(left_mid_point, bottom_mid_point),
        ]

        self.children = [
            QuadTree(
                bound,
                max_objects=self.max_objects,
                depth=self.depth + 1,
                max_depth=self.max_depth,
                objects=[],
                children=[],
            )
            for bound in child_bounds
        ]
        for object in self.objects:
            for child in self.children:
                child.insert(object)
        self.objects = []

    def __query_rec(
        self, shape: Shape, found_objects: list[SpatialObject]
    ) -> list[SpatialObject]:
        if not self.bounds.collides_with(shape):
            return
        found_objects.extend(
            object
            for object in self.objects
            if (object not in found_objects)
            and (object.bounding_box.collides_with(shape))
        )
        found_objects.extend(
            object
            for child in self.children
            for object in child.__query_rec(shape, found_objects)
            if (object not in found_objects)
        )
        yield from found_objects

    def __remove_rec(self, object: SpatialObject) -> bool:
        if object in self.objects:
            object.unsubscribe(self)
            self.objects.remove(object)
            return True
        removed = False
        for child in self.children:
            if child.__remove_rec(object):
                object.unsubscribe(self)
                removed = True
        return removed

    def insert(self, object: SpatialObject) -> bool:
        if not self.bounds.collides_with(object.bounding_box):
            return False
        if object in self.objects:
            return False
        if len(self.objects) < self.max_objects:
            self.objects.append(object)
            self._all_objects.append(object)
            return True
        if not self.children:
            self.__divide()
        inserted = any(child.insert(object) for child in self.children)
        if inserted:
            self._all_objects.append(object)
        return inserted

    def remove(self, object: SpatialObject) -> bool:
        removed = self.__remove_rec(object)
        if removed:
            self._all_objects.remove(object)
        return removed

    def get_objects(self):
        return self._all_objects

    def query(self, shape: Shape) -> list[SpatialObject]:
        yield from self.__query_rec(shape, [])

    def empty_copy(self) -> "QuadTree":
        return QuadTree(
            bounds=self.bounds,
            max_objects=self.max_objects,
            depth=self.depth,
            max_depth=self.max_depth,
        )
