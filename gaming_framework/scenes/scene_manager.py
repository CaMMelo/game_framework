from dataclasses import dataclass

from gaming_framework.scenes.scene import Scene
from gaming_framework.scenes.scene_stack import SceneStack


@dataclass
class SceneManager:
    scene_stack: SceneStack
    scenes: dict[str, Scene]

    def register_scene(self, scene_name: str, scene: Scene):
        self.scenes[scene_name] = scene

    def update(self, delta_time: float):
        current_scene = self.scene_stack.peek()
        current_scene.update(delta_time)

    def draw(self):
        current_scene = self.scene_stack.peek()
        current_scene.draw()
