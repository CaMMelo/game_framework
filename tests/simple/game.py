from dataclasses import dataclass, field

from gaming_framework.physics.body import Body, CollisionHandler


@dataclass
class GameObject(CollisionHandler):
    body: Body


@dataclass
class Coin(GameObject):
    def __post_init__(self):
        super().__post_init__()
        self.collision_resolution_method_name = "resolve_collision_with_coin"


@dataclass
class Enemy(GameObject):
    def __post_init__(self):
        super().__post_init__()
        self.collision_resolution_method_name = "resolve_collision_with_enemy"


@dataclass
class AwarenessSpace(GameObject):
    def resolve_collision_with_coin(self, coin):
        # points to the coin with a yellow flag or something
        ...

    def resolve_collision_with_enemy(self, enemy):
        # points to the enemy with a red flag or something
        ...


@dataclass
class PlayerState:
    collected_coins: int = 0
    health: int = 100


@dataclass
class Player(GameObject):
    awareness_space: AwarenessSpace
    presentation = None
    keyboard_handler = None
    mouse_handler = None
    player_state: PlayerState = None

    def resolve_collision_with_coin(self, coin: Coin):
        print("Hey you found yourself a coin")
        # increment collected coins
        # destroy coin
        ...

    def resolve_collision_with_enemy(self, enemy: Enemy):
        print("Oh no! You were striked by a enemy :(")
        # decrement health
        # decrement enemy health
        ...

    def update(self, delta_time):
        # here is where the keyboard should be processed
        # updating the players body and awareness_space position together
        # this should also update some presentation objects to some state
        ...


@dataclass
class B:
    collision_handler: object = field(init=False, default=None)


player = Player(B(), AwarenessSpace(B()))
coin = Coin(B())
enemy = Enemy(B())

player.resolve_collision(coin)
player.resolve_collision(enemy)
