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
    plateau = mission["plateau"]
    final_positions = []

    for rover in mission["rovers"]:
        final_position = execute_instructions(
            rover["position"],
            rover["instructions"],
            plateau,
        )

        final_positions.append(final_position)

    return final_positions
