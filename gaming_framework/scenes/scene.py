from dataclasses import dataclass

from gaming_framework.scenes.layer import Layer


@dataclass
class Scene:
    objects: list[object]
    layers: list[Layer]

    def update(self, delta_time: float):
        for object in self.objects:
            object.update(delta_time)

    def draw(self):
        for layer in self.layers:
            layer.draw()
