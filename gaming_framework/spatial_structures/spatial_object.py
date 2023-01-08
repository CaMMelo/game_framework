from gaming_framework.geometry.shape import Shape
from gaming_framework.system.events import EventPublisher


class SpatialObject(EventPublisher):
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def bounding_box(self) -> Shape:
        raise NotImplementedError()
