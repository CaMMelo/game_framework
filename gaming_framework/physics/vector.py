from gaming_framework.geometry.shape import Point2D


class Vector2D(Point2D):
    def scalar_mult(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def scalar_div(self, scalar):
        return self.scalar_mult(1 / scalar)
