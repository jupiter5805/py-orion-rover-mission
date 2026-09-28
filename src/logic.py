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

    return {
        "x": position["x"] + dx,
        "y": position["y"] + dy,
        "direction": position["direction"],
    }
