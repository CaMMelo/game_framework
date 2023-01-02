from dataclasses import dataclass

from gaming_framework.geometry.shape import Point2D, Shape


@dataclass
class CollisionShape:
    shape: Shape

    @property
    def bounding_box(self):
        return self.shape.bounding_box

    @property
    def position(self):
        return self.shape.center

    def set_position(self, position):
        if position == self.position:
            return
        self.shape = self.shape.center_to(position)

    def collides_with(self, collision_shape):
        return self.shape.collides_with(collision_shape.shape)
