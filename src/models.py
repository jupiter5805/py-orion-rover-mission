import logging


logger = logging.getLogger(__name__)


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


class Rover:
    DIRECTIONS = ["N", "E", "S", "W"]

    MOVEMENTS = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
    }

    def __init__(self, position):
        self.position = position

    def rotate(self, instruction):
        current_index = self.DIRECTIONS.index(
            self.position.direction
        )

        if instruction == "L":
            new_index = (current_index - 1) % len(self.DIRECTIONS)
        else:
            new_index = (current_index + 1) % len(self.DIRECTIONS)

        self.position.direction = self.DIRECTIONS[new_index]

    def move(self, plateau):
        dx, dy = self.MOVEMENTS[self.position.direction]

        proposed_position = Position(
            self.position.x + dx,
            self.position.y + dy,
            self.position.direction,
        )

        if plateau.contains(proposed_position):
            self.position = proposed_position
        else:
            logger.warning(
                "Move refused: rover at (%s, %s) facing %s would leave plateau",
                self.position.x,
                self.position.y,
                self.position.direction,
            )

    def execute_instructions(self, instructions, plateau):
        for instruction in instructions:
            if instruction in ("L", "R"):
                self.rotate(instruction)
            elif instruction == "M":
                self.move(plateau)

        return self.position
