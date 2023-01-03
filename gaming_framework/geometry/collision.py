import numpy as np

# USED TO HANDLE FLOAT IMPRECISION
FLOAT_TOLERANCE = 0.000000000000001


def point_to_point_collision(point, other):
    return point.x == other.x and point.y == other.y


def point_to_line_collision(point, line):
    d1 = np.linalg.norm(np.array(point) - np.array(line.a))
    d2 = np.linalg.norm(np.array(point) - np.array(line.b))
    line_size = np.linalg.norm(np.array(line.b) - np.array(line.a))
    return (d1 + d2) == line_size


def point_to_circle_collision(point, circle):
    distance = np.linalg.norm(np.array(circle.center) - np.array(point))
    return distance <= (circle.radius + FLOAT_TOLERANCE)


def point_to_rectangle_collision(point, rectangle):
    within_x = rectangle.top_left.x <= point.x <= rectangle.bottom_right.x
    within_y = rectangle.bottom_right.y <= point.y <= rectangle.top_left.y
    return within_x and within_y


def point_to_polygon_collision(point, polygon):
    count = 0
    for line in polygon.lines:
        point_n = np.array(np.array(line.a) - np.array(line.b))
        product = np.dot(point_n, point)
        if product > 0:
            count += 1
    return count % 2 == 1


def line_to_line_collision(line, other):
    ab = np.array(line.b) - np.array(line.a)
    cd = np.array(other.b) - np.array(other.a)
    ab_cross_cd = np.cross(ab, cd)
    if ab_cross_cd == 0:
        return False
    ac = np.array(other.a) - np.array(line.a)
    t1 = np.cross(ac, cd) / ab_cross_cd
    t2 = np.cross(-ab, ac) / ab_cross_cd
    return (0 <= t1 <= 1) and (0 <= t2 <= 1)


def line_to_circle_collision(line, circle):
    if point_to_circle_collision(line.a, circle):
        return True
    if point_to_circle_collision(line.b, circle):
        return True
    distance = np.linalg.norm(line.a - line.b)
    product = np.dot(circle.center - line.a, line.b - line.a) / distance**2
    closest_px = line.a.x + (product * (line.b.x - line.a.x))
    closets_py = line.a.y + (product * (line.b.y - line.a.y))
    closest_point = (closest_px, closets_py)
    if point_to_line_collision(closest_point, line) == False:
        return False
    distance = np.linalg.norm(circle.center - closest_point)
    return distance <= circle.radius


def line_to_rectangle_collision(line, rectangle):
    if point_to_rectangle_collision(line.a, rectangle):
        return True
    if point_to_rectangle_collision(line.b, rectangle):
        return True
    for rect_line in rectangle.lines:
        if line_to_line_collision(line, rect_line):
            return True
    return False


def line_to_polygon_collision(line, polygon):
    for polygon_line in polygon.lines:
        if line_to_line_collision(line, polygon_line):
            return True
    if point_to_polygon_collision(line.a, polygon):
        return True
    if point_to_polygon_collision(line.b, polygon):
        return True
    return False


def circle_to_circle_collision(circle, other):
    distance = np.linalg.norm(circle.center - other.center)
    return distance <= circle.radius + other.radius


def circle_to_rectangle_collision(circle, rectangle):
    testx, testy = circle.center
    if circle.center.x < rectangle.top_left.x:
        testx = rectangle.top_left.x
    if circle.center.x > rectangle.bottom_right.x:
        testx = rectangle.bottom_right.x
    if circle.center.y > rectangle.top_left.y:
        testy = rectangle.top_left.y
    if circle.center.y < rectangle.bottom_right.y:
        testy = rectangle.bottom_right.y
    distance = np.linalg.norm(np.array(circle.center) - np.array((testx, testy)))
    return distance <= circle.radius


def circle_to_polygon_collision(circle, polygon):
    if point_to_polygon_collision(circle.center, polygon):
        return True
    for line in polygon.lines:
        if line_to_circle_collision(line, circle):
            return True
    return False


def rectangle_to_rectangle_collision(rectangle, other):
    return (
        rectangle.bottom_right.x >= other.top_left.x
        and rectangle.top_left.x <= other.bottom_right.x
        and rectangle.bottom_right.y <= other.top_left.y
        and rectangle.top_left.y >= other.bottom_right.y
    )


def rectangle_to_polygon_collision(rectangle, polygon):
    for line in polygon.lines:
        if line_to_rectangle_collision(line, rectangle):
            return True
    return point_to_polygon_collision(rectangle.top_left, polygon)


def polygon_to_polygon_collision(polygon, other):
    for line in polygon.lines:
        if line_to_polygon_collision(line, other):
            return True
    return point_to_polygon_collision(other.points[0], polygon)
