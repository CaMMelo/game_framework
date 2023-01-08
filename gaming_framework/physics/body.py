from dataclasses import dataclass, field

from gaming_framework.geometry.shape import Point2D
from gaming_framework.physics.collision_shape import CollisionShape
from gaming_framework.spatial_structures.spatial_object import SpatialObject


class CollisionHandler:
    collision_resolution_method_name: str = field(init=False, default="")

    def resolve_collision(self, other: "CollisionHandler"):
        collision_resolution_method = getattr(
            self, other.collision_resolution_method_name, None
        )
        if callable(collision_resolution_method):
            collision_resolution_method(other)


@dataclass
class Body(SpatialObject):
    collision_shape: CollisionShape

    speed: Point2D = Point2D(0, 0)
    acceleration: Point2D = Point2D(0, 0)
    mass: float = 1

    is_static: bool = False
    is_tangible: bool = True
    collision_handler: CollisionHandler = field(init=False, default=None)

    def __hash__(self) -> int:
        return id(self)

    def __eq__(self, other: "Body") -> bool:
        return id(self) == id(other)

    def __repr__(self) -> str:
        return (
            "Body(\n"
            f"  collision_shape={self.collision_shape},\n"
            f"  speed={self.speed},\n"
            f"  acceleration={self.acceleration},\n"
            f"  mass={self.mass},\n"
            f"  is_static={self.is_static},\n"
            f"  is_tangible={self.is_tangible},\n"
            ")"
        )

    @property
    def position(self):
        return self.collision_shape.position

    @property
    def bounding_box(self):
        return self.collision_shape.bounding_box

    @property
    def shape(self):
        return self.collision_shape.shape

    def set_position(self, position: Point2D):
        self.collision_shape.set_position(position)

    def predict_position(self, delta_time: float) -> Point2D:
        if self.is_static:
            return self.position
        speed = self.speed + self.acceleration.scalar_mult(delta_time)
        return self.position + speed.scalar_mult(delta_time)

    def move_to(self, position: Point2D):
        old_position = self.position
        self.set_position(position)
        self.publish("moved_to", self, old_position, position)

    def update(self, delta_time: float):
        if self.is_static:
            return
        self.speed += self.acceleration.scalar_mult(delta_time)
        resulting_speed = self.speed.scalar_mult(delta_time)
        position = self.position + resulting_speed
        self.move_to(position)

    def handle_collision(self, body: "Body"):
        if body.collision_handler and self.collision_handler:
            self.collision_handler.resolve_collision(body.collision_handler)
