from src.exceptions import (
    InvalidPlateauError,
    InvalidPositionError,
    InvalidInstructionError,
    InvalidMissionError,
)


VALID_DIRECTIONS = {"N", "E", "S", "W"}
VALID_INSTRUCTIONS = {"L", "R", "M"}


def parse_plateau(text):
    parts = text.split()

    if len(parts) != 2:
        raise InvalidPlateauError(
            f"Plateau must contain two coordinates: '{text}'"
        )

    try:
        max_x = int(parts[0])
        max_y = int(parts[1])
    except ValueError as error:
        raise InvalidPlateauError(
            f"Plateau coordinates must be integers: '{text}'"
        ) from error

    return {"max_x": max_x, "max_y": max_y}


def parse_position(text):
    parts = text.split()

    if len(parts) != 3:
        raise InvalidPositionError(
            f"Position must contain x, y and direction: '{text}'"
        )

    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError as error:
        raise InvalidPositionError(
            f"Position coordinates must be integers: '{text}'"
        ) from error

    direction = parts[2]

    if direction not in VALID_DIRECTIONS:
        raise InvalidPositionError(
            f"Unknown direction: '{direction}'"
        )

    return {
        "x": x,
        "y": y,
        "direction": direction,
    }


def parse_instructions(text):
    instructions = list(text.strip())

    for instruction in instructions:
        if instruction not in VALID_INSTRUCTIONS:
            raise InvalidInstructionError(
                f"Unknown instruction: '{instruction}' in '{text}'"
            )

    return instructions


def parse_mission(text):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        raise InvalidMissionError("Mission input cannot be empty")

    plateau = parse_plateau(lines[0])
    rover_lines = lines[1:]

    if len(rover_lines) % 2 != 0:
        raise InvalidMissionError(
            "Each rover must have a position line and an instruction line"
        )

    rovers = []

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
