import logging
from src.models import Position, Plateau, Rover


logger = logging.getLogger(__name__)
DIRECTIONS = ["N", "E", "S", "W"]


def rotate(position, instruction):
    current_direction = position["direction"]
    current_index = DIRECTIONS.index(current_direction)

    if instruction == "L":
        new_index = (current_index - 1) % len(DIRECTIONS)
    else:
        new_index = (current_index + 1) % len(DIRECTIONS)

    new_direction = DIRECTIONS[new_index]

    return {
        "x": position["x"],
        "y": position["y"],
        "direction": new_direction,
    }


MOVEMENTS = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


def move(position, plateau):
    dx, dy = MOVEMENTS[position["direction"]]

    new_x = position["x"] + dx
    new_y = position["y"] + dy

    if not (
        0 <= new_x <= plateau["max_x"]
        and 0 <= new_y <= plateau["max_y"]
    ):
        logger.warning(
            "Move refused: rover at (%s, %s) facing %s would leave plateau",
            position["x"],
            position["y"],
            position["direction"],
        )
        return position

    return {
        "x": new_x,
        "y": new_y,
        "direction": position["direction"],
    }


def execute_instructions(position, instructions, plateau):
    current_position = position.copy()

    for instruction in instructions:
        if instruction in ("L", "R"):
            current_position = rotate(current_position, instruction)
        elif instruction == "M":
            current_position = move(current_position, plateau)

    return current_position


def run_mission(mission):
    plateau_data = mission["plateau"]

    plateau = Plateau(
        plateau_data["max_x"],
        plateau_data["max_y"],
    )

    final_positions = []

    for rover_data in mission["rovers"]:
        position_data = rover_data["position"]

        position = Position(
            position_data["x"],
            position_data["y"],
            position_data["direction"],
        )

        rover = Rover(position)

        final_position = rover.execute_instructions(
            rover_data["instructions"],
            plateau,
        )

        final_positions.append(
            {
                "x": final_position.x,
                "y": final_position.y,
                "direction": final_position.direction,
            }
        )

    return final_positions
