import sys
from random import randint
from uuid import uuid4

import pygame

from gaming_framework.geometry.shape import Circle, Point2D, Rectangle
from gaming_framework.physics.body import Body, CollisionHandler
from gaming_framework.physics.collision_shape import CollisionShape
from gaming_framework.physics.world import World
from gaming_framework.spatial_structures.spatial_hash import SpatialHash

size = width, height = 320, 240


class Ball(CollisionHandler):
    def __init__(self, body: Body):
        self.body = body
        self.body.collision_handler = self
        self.collision_resolution_method_name = "resolve_collision_with_ball"
        self.id = uuid4()
        self.color = (255, 255, 255)

    def resolve_collision_with_wall(self, wall):
        if (
            self.body.shape.center.x + self.body.shape.radius
        ) >= wall.body.shape.top_left.x:
            self.color = (
                (255, 0, 0) if self.color == (255, 255, 255) else (255, 255, 255)
            )
            self.body.speed = Point2D(-self.body.speed.x, self.body.speed.y)

    def update(self, delta_time):
        ...

    def draw(self, screen):
        pygame.draw.circle(
            screen, self.color, self.body.position, self.body.shape.radius, 1
        )


class Wall(CollisionHandler):
    def __init__(self, body: Body):
        self.id = uuid4()
        self.body = body
        self.body.collision_handler = self
        self.collision_resolution_method_name = "resolve_collision_with_wall"
        self.color = (255, 255, 255)

    def update(self, delta_time):
        ...

    def draw(self, screen):
        pg_rect = pygame.Rect(
            self.body.shape.top_left.x,
            height - self.body.shape.top_left.y,
            self.body.shape.width,
            self.body.shape.height,
        )
        pygame.draw.rect(screen, self.color, pg_rect)


area = Rectangle(Point2D(0, height), Point2D(width, 0))
quadtree = SpatialHash(area)
world = World(area, quadtree)

ball_shape = Circle(Point2D(width / 2, height / 2), 20)
ball_collision_shape = CollisionShape(ball_shape)
ball_body = Body(ball_collision_shape, Point2D(200, 0))
ball = Ball(ball_body)

wall_shape = Rectangle(Point2D(width - 8, height), Point2D(width - 2, 0))
wall_collision_shape = CollisionShape(wall_shape)
wall_body = Body(wall_collision_shape, is_static=True)
wall = Wall(wall_body)


quadtree.insert(ball_body)
quadtree.insert(wall_body)


pygame.init()


screen = pygame.display.set_mode((width, height))


previous_tick = 0
while True:
    current_tick = pygame.time.get_ticks()
    delta_time = (current_tick - previous_tick) / 1000
    previous_tick = current_tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    world.update(delta_time)
    ball.update(delta_time)
    wall.update(delta_time)

    screen.fill((0, 0, 0))
    ball.draw(screen)
    wall.draw(screen)

    pygame.display.flip()
