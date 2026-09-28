class Position:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction


class Plateau:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    def contains(self, position):
        return (
            0 <= position.x <= self.max_x
            and 0 <= position.y <= self.max_y
        )
