import heapq
from dataclasses import dataclass, field

import numpy as np

from gaming_framework.geometry.point import Point2D
from gaming_framework.geometry.polygon import Polygon
from gaming_framework.geometry.rectangle import Rectangle
from gaming_framework.physics.body import Body
from gaming_framework.physics.body_pair import BodyPair
from gaming_framework.physics.collision_shape import CollisionShape
from gaming_framework.physics.quadtree import QuadTree


@dataclass
class World:
    visible_area: Rectangle
    quadtree: QuadTree

    moving_bodies: dict = field(init=False, default_factory=dict)
    sweept_bodies: dict = field(init=False, default_factory=dict)
    movement_quadtree: QuadTree = field(init=False, default=None)
    collision_candidates: list = field(init=False, default_factory=list)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    def __calculate_sweept_body(self, body, old_pos, new_pos):
        rectangle = body.bounding_box
        dx = new_pos.x - old_pos.x
        dy = new_pos.y - old_pos.y
        new_points = [point for point in rectangle.points]
        old_points = [Point2D(point.x + dx, point.y + dy) for point in new_points]
        polygon_points = new_points + old_points
        maxx = max(point.x for point in polygon_points)
        minx = min(point.x for point in polygon_points)
        maxy = max(point.y for point in polygon_points)
        miny = min(point.y for point in polygon_points)
        cx = (maxx + minx) / 2
        cy = (maxy + miny) / 2
        polygon_points = sorted(
            [
                point
                for point in polygon_points
                if not ((minx < point.x < maxx) and (miny < point.y < maxy))
            ],
            key=lambda point: np.arctan2(point.y - cy, point.x - cx),
        )
        polygon = Polygon(polygon_points)
        collision_shape = CollisionShape(body.position, polygon)
        return Body(collision_shape)

    def __time_of_moving_collision(self, body_a, body_b, delta_time):
        # 1: check where in time the collision might have occurred
        time_of_collision = 0
        return time_of_collision

    def __time_of_static_collision(self, moving_body, static_body, delta_time):
        # 1: check where in time the collision might have occurred
        time_of_collision = 0
        return time_of_collision

    def __push_to_collision_candidates(
        self, pair, start_time, delta_time, toc_callback
    ):
        toc = toc_callback(pair.body_a, pair.body_b, delta_time)
        if start_time <= toc <= (start_time + delta_time):
            heapq.heappush(self.collision_candidates, (toc, pair))

    def __remove_moving_body(self, body):
        (_, _, sweept_body) = self.moving_bodies[body]
        del self.moving_bodies[body]
        del self.sweept_bodies[sweept_body]
        self.movement_quadtree.remove(sweept_body)
        self.collision_candidates = list(
            filter(
                lambda _, pair: (pair.body_a == body) or (pair.body_b == body),
                self.collision_candidates,
            )
        )

    def __predict_movement(self, body, delta_time):
        new_pos = body.predict_position(delta_time)
        old_pos = body.position
        if new_pos == old_pos:
            return
        sweept_body = self.__calculate_sweept_body(body, old_pos, new_pos)
        self.moving_bodies[body] = (old_pos, new_pos, sweept_body)
        self.sweept_bodies[sweept_body] = body
        self.movement_quadtree.insert(sweept_body)

    def __query_collisions_with_moving_bodies(self, body, delta_time, start_time):
        (_, _, sweept_body) = self.moving_bodies[body]
        pairs = []
        for candidate in (
            BodyPair(body, self.sweept_bodies[sweept_body_b])
            for sweept_body_b in self.movement_quadtree.query(sweept_body.shape)
            if (sweept_body != sweept_body_b)
            and (body != self.sweept_bodies[sweept_body_b])
            and sweept_body.shape.collides_with(sweept_body_b.shape)
        ):
            if candidate not in pairs:
                pairs.append(candidate)
                self.__push_to_collision_candidates(
                    candidate, start_time, delta_time, self.__time_of_moving_collision
                )

    def __query_collisions_with_static_bodies(self, body, delta_time, start_time):
        (_, _, sweept_body) = self.moving_bodies[body]
        pairs = []
        for candidate in (
            BodyPair(body, static_body)
            for static_body in self.quadtree.query(sweept_body.shape)
            if (static_body not in self.moving_bodies)
            and (sweept_body.shape.collides_with(static_body.bounding_box))
        ):
            if candidate not in pairs:
                pairs.append(candidate)
                self.__push_to_collision_candidates(
                    candidate, start_time, delta_time, self.__time_of_static_collision
                )

    def __update_collision_candidates(self, body, delta_time, start_time):
        if body not in self.moving_bodies:
            return
        self.__query_collisions_with_moving_bodies(body, delta_time, start_time)
        self.__query_collisions_with_static_bodies(body, delta_time, start_time)

    def __handle_contact(self, body_a, body_b, current_time, end_time):
        self.__remove_moving_body(body_a)
        self.__remove_moving_body(body_b)
        heapq.heapify(self.collision_candidates)
        remaining_time = end_time - current_time
        self.__predict_movement(body_a, remaining_time)
        self.__predict_movement(body_b, remaining_time)
        self.__update_collision_candidates(body_a, remaining_time, current_time)
        self.__update_collision_candidates(body_b, remaining_time, current_time)

    def __resolve_collision(self, body_a, body_b, current_time, end_time):
        handle_contact = body_a.is_tangible and body_b.is_tangible
        if handle_contact:
            # move body_a, and body_b to their positions in current_time
            # update physical forces working on body_a and body_b
            self.__handle_contact(body_a, body_b, current_time, end_time)
        body_a.handle_collision(body_b)
        body_b.handle_collision(body_a)

    def __check_collision(self, body_a, body_b, current_time, end_time):
        comparing_shape_a = body_a.shape
        comparing_shape_b = body_b.shape
        if body_a in self.moving_bodies:
            # comparing_shape_a = body_a.shape moved to position at time of collision
            ...
        if body_b in self.moving_bodies:
            # comparing_shape_b = body_b.shape moved to position at time of collision
            ...
        if comparing_shape_a.collides_with(comparing_shape_b):
            self.__resolve_collision(body_a, body_b, current_time, end_time)

    def __detect_collisions(self, delta_time):
        while self.collision_candidates:
            time_of_collision, pair = heapq.heappop(self.collision_candidates)
            self.__check_collision(
                pair.body_a, pair.body_b, time_of_collision, delta_time
            )

    def get_visible_bodies(self):
        return self.quadtree.query(self.visible_area)

    def update(self, delta_time):
        self.moving_bodies = {}
        self.sweept_bodies = {}
        self.movement_quadtree = QuadTree(self.quadtree.bounds)
        self.collision_candidates = []
        for body in self.quadtree.objects():
            self.__predict_movement(body, delta_time)
        for body in self.moving_bodies:
            self.__update_collision_candidates(body, delta_time, start_time=0)
        self.__detect_collisions(delta_time)
        # must update all remaining moving objects to their final positions
        ...
