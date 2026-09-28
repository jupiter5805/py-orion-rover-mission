import logging

from src.exceptions import InvalidPositionError, InvalidPlateauError


logger = logging.getLogger(__name__)


class Position:
    VALID_DIRECTIONS = {"N", "E", "S", "W"}

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidPositionError(
                "Position x must be a non-negative integer"
            )

        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if not isinstance(value, int) or value < 0:
            raise InvalidPositionError(
                "Position y must be a non-negative integer"
            )

        self._y = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value not in self.VALID_DIRECTIONS:
            raise InvalidPositionError(
                f"Invalid direction: '{value}'"
            )

        self._direction = value


class Plateau:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    @property
    def max_x(self):
        return self._max_x

    @max_x.setter
    def max_x(self, value):
        if not isinstance(value, int) or value <= 0:
            raise InvalidPlateauError(
                "Plateau max_x must be a positive integer"
            )

        self._max_x = value

    @property
    def max_y(self):
        return self._max_y

    @max_y.setter
    def max_y(self, value):
        if not isinstance(value, int) or value <= 0:
            raise InvalidPlateauError(
                "Plateau max_y must be a positive integer"
            )

        self._max_y = value

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

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if not isinstance(value, Position):
            raise InvalidPositionError(
                "Rover position must be a Position object"
            )

        self._position = value

    def rotate(self, instruction):
        current_index = self.DIRECTIONS.index(
            self.position.direction
        )

        if instruction == "L":
            new_index = (current_index - 1) % len(self.DIRECTIONS)
        else:
            new_index = (current_index + 1) % len(self.DIRECTIONS)

        self.position.direction = self.DIRECTIONS[new_index]

    def _move_by_distance(self, plateau, distance):
        dx, dy = self.MOVEMENTS[self.position.direction]

        new_x = self.position.x + (dx * distance)
        new_y = self.position.y + (dy * distance)

        if not (
            0 <= new_x <= plateau.max_x
            and 0 <= new_y <= plateau.max_y
        ):
            logger.warning(
                "Move refused: rover at (%s, %s) facing %s "
                "would leave plateau",
                self.position.x,
                self.position.y,
                self.position.direction,
            )
            return

        self.position = Position(
            new_x,
            new_y,
            self.position.direction,
        )

    def move(self, plateau):
        self._move_by_distance(plateau, 1)

    def execute_instructions(self, instructions, plateau):
        for instruction in instructions:
            if instruction in ("L", "R"):
                self.rotate(instruction)
            elif instruction == "M":
                self.move(plateau)

        return self.position


class CargoRover(Rover):
    def move(self, plateau):
        self._move_by_distance(plateau, 2)
