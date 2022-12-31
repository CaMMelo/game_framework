from dataclasses import dataclass, field

from gaming_framework.physics.collision_shape import CollisionShape
from gaming_framework.physics.quadtree import QuadTreeObject
from gaming_framework.physics.vector import Vector2D


class CollisionHandler:
    collision_resolution_method_name: str = field(init=False, default="")

    def resolve_collision(self, collision_handler):
        collision_resolution_method = getattr(
            self, collision_handler.collision_resolution_method_name, None
        )
        if callable(collision_resolution_method):
            collision_resolution_method(collision_handler)


@dataclass
class Body(QuadTreeObject):
    collision_shape: CollisionShape

    speed: Vector2D = Vector2D(0, 0)
    acceleration: Vector2D = Vector2D(0, 0)
    mass: float = 0

    is_static: bool = False
    is_tangible: bool = True
    collision_handler: CollisionHandler = field(init=False, default=None)

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def position(self):
        x = self.collision_shape.position.x
        y = self.collision_shape.position.y
        return Vector2D(x, y)

    @property
    def bounding_box(self):
        return self.collision_shape.bounding_box

    @property
    def shape(self):
        return self.collision_shape.shape

    def set_position(self, position):
        self.collision_shape.set_position(position)

    def predict_position(self, delta_time):
        if self.is_static:
            return self.position
        speed = self.speed + self.acceleration.scalar_mult(delta_time)
        return self.position + speed.scalar_mult(delta_time)

    def move_to(self, position):
        old_position = self.position
        self.set_position(position)
        self.publish("moved_to", old_position, position)

    def update(self, delta_time):
        if self.is_static:
            return
        self.speed += self.acceleration.scalar_mult(delta_time)
        resulting_speed = self.speed.scalar_mult(delta_time)
        position = self.position + resulting_speed
        self.move_to(position)

    def handle_collision(self, body):
        if body.collision_handler and self.collision_handler:
            self.collision_handler.resolve_collision(body.collision_handler)
