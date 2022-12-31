from dataclasses import dataclass

from gaming_framework.scenes.scene import Scene


@dataclass
class SceneStack:
    stack: list[Scene]

    def push(self, scene):
        self.stack.append(scene)

    def pop(self):
        if self.stack:
            self.stack.pop()

    def peek(self):
        return self.stack[-1]
