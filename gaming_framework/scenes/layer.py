from dataclasses import dataclass


@dataclass
class Layer:
    is_visible: bool = True

    def show(self):
        self.is_visible = True

    def hide(self):
        self.is_visible = False

    def draw(self):
        ...
