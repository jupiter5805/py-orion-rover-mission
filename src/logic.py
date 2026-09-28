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
