def parse_plateau(text):
    parts = text.split()

    max_x = int(parts[0])
    max_y = int(parts[1])

    return {"max_x": max_x, "max_y": max_y}


def parse_position(text):
    parts = text.split()

    x = int(parts[0])
    y = int(parts[1])
    direction = parts[2]

    return {"x": x, "y": y, "direction": direction}


def parse_instructions(text):
    instructions = list(text)

    return instructions


def parse_mission(text):
    lines = text.splitlines()

    plateau = parse_plateau(lines[0])
    rovers = []

    rover_lines = lines[1:]

    for index in range(0, len(rover_lines), 2):
        position_line = rover_lines[index]
        instructions_line = rover_lines[index + 1]

        rover = {
            "position": parse_position(position_line),
            "instructions": parse_instructions(instructions_line),
        }

        rovers.append(rover)

    return {
        "plateau": plateau,
        "rovers": rovers,
    }
