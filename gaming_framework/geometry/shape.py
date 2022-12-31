class Shape:
    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @property
    def bounding_box(self):
        raise NotImplementedError()

    def center_to(self, point):
        raise NotImplementedError()

    def point_collision(self, point):
        raise NotImplementedError()

    def line_collision(self, line):
        raise NotImplementedError()

    def circle_collision(self, circle):
        raise NotImplementedError()

    def rectangle_collision(self, rectangle):
        raise NotImplementedError()

    def polygon_collision(self, polygon):
        raise NotImplementedError()

    def collides_with(self, shape):
        raise NotImplementedError()
