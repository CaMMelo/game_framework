from dataclasses import dataclass

from gaming_framework.geometry.point import Point2D
from gaming_framework.geometry.shape import Shape


@dataclass
class CollisionShape:
    position: Point2D
    shape: Shape

    @property
    def bounding_box(self):
        return self.shape.bounding_box

    def set_position(self, position):
        if position == self.position:
            return
        self.position = position
        self.shape = self.shape.center_to(self.position)

    def collides_with(self, collision_shape):
        return self.shape.collides_with(collision_shape.shape)
