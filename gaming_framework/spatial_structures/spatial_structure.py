from gaming_framework.geometry.shape import Shape
from gaming_framework.spatial_structures.spatial_object import SpatialObject


class SpatialStructure:
    def insert(self, object: SpatialObject):
        raise NotImplementedError()

    def remove(self, object: SpatialObject):
        raise NotImplementedError()

    def get_objects(self):
        raise NotImplementedError()

    def query(self, shape: Shape):
        raise NotImplementedError()
    
    def empty_copy(self):
        raise NotImplementedError()
