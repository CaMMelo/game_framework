from gaming_framework.geometry.shape import (
    Circle,
    Line2D,
    Point2D,
    Polygon,
    Rectangle,
    ShapeVisitor,
)


class CircleBoundingBox(ShapeVisitor):
    # TODO!!!!: remove object from memory when its not needed anymore
    def __init__(self):
        self.memory = {}

    def accept_point(self, point: Point2D):
        if point in self.memory:
            return self.memory[point]
        self.memory[point] = Circle(self, 1)
        return self.memory[point]

    def accept_line(self, line: Line2D):
        if line in self.memory:
            return self.memory[line]
        radius = line.size / 2
        self.memory[line] = Circle(line.center, radius)
        return self.memory[line]

    def accept_circle(self, circle: Circle):
        return circle

    def accept_rectangle(self, rectangle: Rectangle):
        if rectangle in self.memory:
            return self.memory[rectangle]
        radius = rectangle.top_left.distance(rectangle.bottom_right) / 2
        self.memory[rectangle] = Circle(rectangle.center, radius)
        return self.memory[rectangle]

    def accept_polygon(self, polygon: Polygon):
        if polygon in self.memory:
            return self.memory[polygon]
        top = max(point.y for point in polygon.points)
        left = min(point.x for point in polygon.points)
        bottom = min(point.y for point in polygon.points)
        right = max(point.x for point in polygon.points)
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        center = (top_left + bottom_right).scalar_div(2)
        radius = top_left.distance(bottom_right) / 2
        self.memory[polygon] = Circle(center, radius)
        return self.memory[polygon]


class RectangleBoundingBox(ShapeVisitor):
    def __init__(self):
        self.memory = {}

    def accept_point(self, point: Point2D):
        if point in self.memory:
            return self.memory[point]
        top = point.y + 1
        left = point.x - 1
        bottom = point.y - 1
        right = point.x + 1
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        self.memory[point] = Rectangle(top_left, bottom_right)
        return self.memory[point]

    def accept_line(self, line: Line2D):
        if line in self.memory:
            return self.memory[line]
        top = max(line.a.y, line.b.y)
        left = min(line.a.x, line.b.x)
        bottom = min(line.a.y, line.b.y)
        right = max(line.a.x, line.b.x)
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        self.memory[line] = Rectangle(top_left, bottom_right)
        return self.memory[line]

    def accept_circle(self, circle: Circle):
        if circle in self.memory:
            return self.memory[circle]
        top = circle.center.y + circle.radius
        left = circle.center.x - circle.radius
        bottom = circle.center.y - circle.radius
        right = circle.center.y + circle.radius
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        self.memory[circle] = Rectangle(top_left, bottom_right)
        return self.memory[circle]

    def accept_rectangle(self, rectangle: Rectangle):
        return rectangle

    def accept_polygon(self, polygon: Polygon):
        if polygon in self.memory:
            return self.memory[polygon]
        top = max(point.y for point in polygon.points)
        left = min(point.x for point in polygon.points)
        bottom = min(point.y for point in polygon.points)
        right = max(point.x for point in polygon.points)
        top_left = Point2D(left, top)
        bottom_right = Point2D(right, bottom)
        self.memory[polygon] = Rectangle(top_left, bottom_right)
        return self.memory[polygon]
