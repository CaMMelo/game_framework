from dataclasses import dataclass

from gaming_framework.geometry.shape import Point2D, Rectangle
from gaming_framework.system.events import EventPublisher


class QuadTreeObject(EventPublisher):
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def bounding_box(self):
        raise NotImplementedError()


@dataclass
class QuadTreeNode(EventPublisher):
    bounds: Rectangle
    max_objects: int
    max_depth: int
    objects: list[QuadTreeObject]
    children: list["QuadTreeNode"]

    def __post_init__(self):
        for object in self.objects:
            self.insert(object)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def __handle_object_moved_to(self, object, old_pos, new_pos):
        if not self.bounds.collides_with(object.bounding_box):
            self.__move_object_out(object, old_pos, new_pos)

    def __insert_rec(self, object, depth):
        if not self.bounds.collides_with(object.bounding_box):
            return False
        if object in self.objects:
            return False
        if (len(self.objects) < self.max_objects) or depth >= self.max_depth:
            self.__subscribe_to_object_events(object)
            self.objects.append(object)
            return True
        if not self.children:
            self.divide()
        # if the object collides with more than one quadrant I want that object
        # to be a part of both quadrants, so I insert it in both of them
        inserted = any(
            [child.__insert_rec(object, depth=depth + 1) for child in self.children]
        )
        if inserted:
            self.__subscribe_to_object_events(object)
        return inserted

    def __query_rec(self, shape, found_objects):
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
        )
        yield from found_objects

    def __subscribe_to_object_events(self, object):
        object.subscribe("moved_to", self, self.__handle_object_moved_to)

    def __remove_rec(self, object):
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

    def __move_object_out(self, object, old_pos, new_pos):
        if self.objects.__remove_rec(object):
            self.publish("object_moved_out", object, old_pos, new_pos)

    def __get_objects(self):
        objects = self.objects
        objects.extend(
            object
            for child in self.children
            for object in child.__get_objects()
            if object not in objects
        )
        yield from objects

    def objects(self):
        yield from self.__get_objects()

    def divide(self):
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
            QuadTreeNode(
                bound,
                max_objects=self.max_objects,
                max_depth=self.max_depth,
            )
            for bound in child_bounds
        ]
        for object in self.objects:
            for child in self.children:
                child.insert(object)
        self.objects = []

        self.publish("node_divided", self.children)

    def insert(self, object):
        return self.__insert_rec(object, 0)

    def remove(self, object):
        removed = self.__remove_rec(object)
        if removed:
            self.publish("object_removed", object)
        return removed

    def query(self, shape):
        yield from self.__query_rec(shape, [])


class QuadTree(EventPublisher):
    def __init__(
        self,
        bounds: Rectangle,
        max_objects: int = 4,
        max_depth: int = 5,
        objects: list[QuadTreeObject] = None,
        children: list[QuadTreeNode] = None,
    ):
        self.max_objects = max_objects
        self.max_depth = max_depth
        self.root_node = QuadTreeNode(
            bounds,
            max_objects,
            max_depth,
            objects or [],
            children or [],
        )
        self.__subscribe_to_node_events(self.root_node)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def bounds(self):
        return self.bounds

    def __handle_object_removed(self, _, object):
        self.publish("object_removed", object)

    def __handle_object_moved_out(self, _, object):
        self.insert(object)

    def __handle_node_divided(self, _, children):
        for child in children:
            self.__subscribe_to_node_events(child)

    def __subscribe_to_node_events(self, node):
        node.subscribe("object_removed", self, self.__handle_object_removed)
        node.subscribe("object_moved_out", self, self.__handle_object_moved_out)
        node.subscribe("node_divided", self, self.__handle_node_divided)

    def __span_quadrant(self, quadrant, relative_to):
        dx = abs(self.bounds.top_left.x - self.bounds.bottom_right.x)
        dy = abs(self.bounds.top_left.y - self.bounds.bottom_right.y)
        top = self.bounds.top_left.y
        left = self.bounds.top_left.x
        bottom = self.bounds.bottom_right.y
        right = self.bounds.bottom_right.x
        if quadrant == 0:
            if relative_to == 1 or relative_to == 2:
                left = left - dx
                right = left - dx
            if relative_to == 2 or relative_to == 3:
                top = top + dy
                bottom = bottom + dy
        elif quadrant == 1:
            if relative_to == 0 or relative_to == 3:
                left = left + dx
                right = right + dx
            if relative_to == 2 or relative_to == 3:
                top = top + dy
                bottom = bottom + dy
        elif quadrant == 2:
            if relative_to == 0 or relative_to == 3:
                left = left + dx
                right = right + dx
            if relative_to == 0 or relative_to == 1:
                top = top - dy
                bottom = bottom - dy
        elif quadrant == 3:
            if relative_to == 0 or relative_to == 1:
                top = top - dy
                bottom = bottom - dy
            if relative_to == 1 or relative_to == 2:
                left = left - dx
                right = right - dx
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        return Rectangle(top_left, bottom_right)

    def __find_relative_quadrant(self, object):
        is_up = object.bounding_box.center.y <= self.bounds.center.y
        is_left = object.bounding_box.center.x <= self.bounds.center.x
        if is_left:
            if is_up:
                return 2
            else:
                return 1
        else:
            if is_up:
                return 3
            else:
                return 0

    def __update_bounds(self, object):
        current_quadrant = self.__find_relative_quadrant(object)
        children_bounds: list[Rectangle] = []
        for quadrant in range(4):
            if quadrant != current_quadrant:
                bounds = self.__span_quadrant(quadrant, current_quadrant)
                children_bounds.append(bounds)
        children = [
            QuadTreeNode(
                bound,
                max_objects=self.max_objects,
                max_depth=self.max_depth,
            )
            for bound in children_bounds
        ]
        children.insert(current_quadrant, self.root_node)
        top_left = children_bounds[0].top_left
        bottom_right = children_bounds[2].top_left
        parent_bounds = Rectangle(top_left, bottom_right)
        parent_node = QuadTreeNode(
            parent_bounds,
            max_objects=self.max_objects,
            max_depth=self.max_depth,
            children=children,
        )
        self.root_node = parent_node

    def objects(self):
        yield from self.root_node.objects()

    def insert(self, object):
        if self.bounds.collides_with(object.bounding_box):
            self.publish("object_inserted", object)
            return self.root_node.insert(object)
        self.__update_bounds(object)
        return self.insert(object)

    def remove(self, object):
        self.root_node.remove(object)

    def query(self, shape):
        yield from self.root_node.query(shape)
