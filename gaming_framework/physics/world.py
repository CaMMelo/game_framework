import heapq
from dataclasses import dataclass, field

import numpy as np

from gaming_framework.geometry.shape import Point2D, Rectangle
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

    def __calculate_sweept_body(self, body: Body, new_pos: Point2D):
        top = body.bounding_box.center.y + body.bounding_box.radius
        left = body.bounding_box.center.x - body.bounding_box.radius
        bottom = new_pos.center.y - body.bounding_box.radius
        right = new_pos.center.x + body.bounding_box.radius
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        sweept_shape = Rectangle(top_left, bottom_right)
        collision_shape = CollisionShape(sweept_shape)
        sweept_body = Body(collision_shape)
        return sweept_body

    def __time_of_collision(self, body_a: Body, body_b: Body):
        distance = body_a.position.distance(body_b.position)
        squared_speed_body_a = body_a.speed.x**2 + body_a.speed.y**2
        squared_accel_body_a = body_a.acceleration.x**2 + body_a.acceleration.y**2
        squared_speed_body_b = body_b.speed.x**2 + body_b.speed.y**2
        squared_accel_body_b = body_b.acceleration.x**2 + body_b.acceleration.y**2

        delta_speed = abs(squared_speed_body_a - squared_speed_body_b)
        delta_accel = abs(squared_accel_body_a - squared_accel_body_b)

        time_of_collision = np.sqrt((2 * distance * delta_speed) / delta_accel)

        return time_of_collision

    def __push_to_collision_candidates(self, pair, delta_time, start_time):
        toc = self.__time_of_collision(pair.body_a, pair.body_b)
        if toc <= (start_time + delta_time):
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
        if new_pos == body.position:
            return
        sweept_body = self.__calculate_sweept_body(body, new_pos)
        self.moving_bodies[body] = (body.position, new_pos, sweept_body)
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
        ):
            if candidate not in pairs:
                pairs.append(candidate)
                self.__push_to_collision_candidates(candidate, delta_time, start_time)

    def __query_collisions_with_static_bodies(self, body, delta_time, start_time):
        (_, _, sweept_body) = self.moving_bodies[body]
        pairs = []
        for candidate in (
            BodyPair(body, static_body)
            for static_body in self.quadtree.query(sweept_body.shape)
            if (static_body not in self.moving_bodies)
        ):
            if candidate not in pairs:
                pairs.append(candidate)
                self.__push_to_collision_candidates(candidate, delta_time, start_time)

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

    def __update_body_forces(self, body_a, body_b):
        v1 = (
            body_a.mass * body_a.speed
            + body_b.mass * body_b.speed
            + body_b.mass * (body_b.speed - body_a.speed)
        ) / (body_a.mass + body_b.mass)

        v2 = (
            body_a.mass * body_a.speed
            + body_b.mass * body_b.speed
            + body_a.mass * (body_a.speed - body_b.speed)
        ) / (body_a.mass + body_b.mass)

        body_a.speed = v1
        body_b.speed = v2

    def __update_body_position(self, body: Body, current_time: float):
        position = body.predict_position(current_time)
        body.move_to(position)

    def __resolve_collision(
        self, body_a: Body, body_b: Body, current_time: float, end_time: float
    ):
        handle_contact = body_a.is_tangible and body_b.is_tangible
        if handle_contact:
            instant_before = current_time - 0.000000000000001
            self.__update_body_position(body_a, instant_before)
            self.__update_body_position(body_b, instant_before)
            self.__update_body_forces(body_a, body_b)
            self.__handle_contact(body_a, body_b, current_time, end_time)

        body_a.handle_collision(body_b)
        body_b.handle_collision(body_a)

    def __check_collision(
        self, body_a: Body, body_b: Body, time_of_collision: float, delta_time: float
    ):
        comparing_shape_a = body_a.shape
        comparing_shape_b = body_b.shape

        if body_a in self.moving_bodies:
            position = body_a.predict_position(time_of_collision)
            comparing_shape_a = body_a.shape.center_to(position)

        if body_b in self.moving_bodies:
            position = body_b.predict_position(time_of_collision)
            comparing_shape_b = body_b.shape.center_to(position)

        if comparing_shape_a.collides_with(comparing_shape_b):
            self.__resolve_collision(
                body_a, body_b, current_time=time_of_collision, end_time=delta_time
            )

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
        for body in self.quadtree.get_objects():
            self.__predict_movement(body, delta_time)
        for body in self.moving_bodies:
            self.__update_collision_candidates(body, delta_time, start_time=0)
        self.__detect_collisions(delta_time)
        for body in self.moving_bodies:
            self.__update_body_position(body, delta_time)
