from random import randint
from uuid import uuid4

from gaming_framework.geometry.shape import Circle, Point2D, Rectangle
from gaming_framework.physics.body import Body
from gaming_framework.physics.collision_shape import CollisionShape
from gaming_framework.physics.quadtree import QuadTree
from gaming_framework.physics.vector import Vector2D
from gaming_framework.physics.world import World

size = width, height = 320, 240


class Ball:
    def __init__(self, body: Body):
        self.body = body
        self.body.collision_handler = self
        self.collision_resolution_method_name = "resolve_collision_with_ball"
        self.id = uuid4()

    def resolve_collision_with_ball(self, other):
        print(f"{self.id} collides with {other.id}")

    def update(self, delta_time):
        if self.body.position.x + self.body.shape.radius >= width:
            self.body.speed = Vector2D(-self.body.speed.x, self.body.speed.y)
        if self.body.position.x - self.body.shape.radius <= 0:
            self.body.speed = Vector2D(-self.body.speed.x, self.body.speed.y)
        if self.body.position.y + self.body.shape.radius >= height:
            self.body.speed = Vector2D(self.body.speed.x, -self.body.speed.y)
        if self.body.position.y - self.body.shape.radius <= 0:
            self.body.speed = Vector2D(self.body.speed.x, -self.body.speed.y)


area = Rectangle(Point2D(0, height), Point2D(width, 0))
quadtree = QuadTree(area)
world = World(area, quadtree)

circles = [Circle(Point2D(i * 20 + 20, i * 20 + 20), 10) for i in range(10)]
bodies = [
    Body(
        collision_shape=CollisionShape(circle),
        speed=Vector2D(randint(20, 40), randint(20, 40)),
    )
    for circle in circles
]
balls = [Ball(body) for body in bodies]

print("INSERTING BODIES INTO QUADTREE")
for body in bodies:
    quadtree.insert(body)
print("------------------------------")


import sys

import pygame

pygame.init()


screen = pygame.display.set_mode((width * 2, height * 2))
clock = pygame.time.Clock()


def draw_quadtree(node):
    if node.objects:
        rect = pygame.Rect(
            node.bounds.top_left.x,
            node.bounds.top_left.y,
            node.bounds.bottom_right.x - node.bounds.top_left.x,
            node.bounds.top_left.y - node.bounds.bottom_right.y,
        )
        pygame.draw.rect(screen, (100, 100, 100), rect, 1)
    for child in node.children:
        draw_quadtree(child)


previous_tick = 0
while True:
    current_tick = pygame.time.get_ticks()
    delta_time = (current_tick - previous_tick) / 60
    previous_tick = current_tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for ball in balls:
        ball.update(delta_time)
    world.update(delta_time)

    screen.fill((0, 0, 0))
    # draw_quadtree(quadtree.root_node)
    for body in bodies:
        pygame.draw.circle(screen, (255, 255, 255), body.position, body.shape.radius, 1)
    pygame.display.flip()
