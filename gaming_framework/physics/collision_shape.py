from dataclasses import dataclass

from gaming_framework.geometry.shape import Point2D, Shape


@dataclass
class CollisionShape:
    shape: Shape

    @property
    def bounding_box(self) -> Shape:
        return self.shape.bounding_box

    @property
    def position(self) -> Point2D:
        return self.shape.center

    def set_position(self, position: Point2D):
        if position == self.position:
            return
        self.shape = self.shape.center_to(position)

    def collides_with(self, other: "CollisionShape") -> bool:
        return self.shape.collides_with(other.shape)
