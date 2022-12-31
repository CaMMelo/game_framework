from gaming_framework.physics.body import Body


class BodyPair:
    body_a: Body
    body_b: Body

    def __hash__(self):
        return hash((id(self.body_a), id(self.body_b)))

    def __eq__(self, other):
        has_body_a = self.body_a == other.body_a or self.body_a == other.body_b
        has_body_b = self.body_b == other.body_a or self.body_b == other.body_b
        return has_body_a and has_body_b
