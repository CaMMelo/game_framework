from gaming_framework.geometry.point import Point2D


class Vector2D(Point2D):
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def scalar_mult(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __add__(self, other):
        if not other:
            return Vector2D(self.x, self.y)
        return Vector2D(self.x + other.x, self.y + other.y)
