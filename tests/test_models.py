import pytest

from src.models import Position, Plateau, Rover


def test_position_stores_x_coordinate():
    position = Position(1, 2, "N")

    assert position.x == 1


def test_position_stores_y_coordinate():
    position = Position(1, 2, "N")

    assert position.y == 2


def test_position_stores_direction():
    position = Position(1, 2, "N")

    assert position.direction == "N"


def test_position_can_store_different_values():
    position = Position(4, 3, "W")

    assert position.x == 4
    assert position.y == 3
    assert position.direction == "W"


def test_plateau_stores_bounds():
    plateau = Plateau(5, 5)

    assert plateau.max_x == 5
    assert plateau.max_y == 5


def test_plateau_contains_position_inside_bounds():
    plateau = Plateau(5, 5)
    position = Position(2, 3, "N")

    assert plateau.contains(position) is True


def test_plateau_contains_upper_right_corner():
    plateau = Plateau(5, 5)
    position = Position(5, 5, "E")

    assert plateau.contains(position) is True


def test_plateau_rejects_position_past_north_edge():
    plateau = Plateau(5, 5)
    position = Position(2, 6, "N")

    assert plateau.contains(position) is False


def test_plateau_rejects_position_past_east_edge():
    plateau = Plateau(5, 5)
    position = Position(6, 2, "E")

    assert plateau.contains(position) is False


def test_plateau_rejects_negative_x():
    plateau = Plateau(5, 5)
    position = Position(-1, 2, "W")

    assert plateau.contains(position) is False


def test_plateau_rejects_negative_y():
    plateau = Plateau(5, 5)
    position = Position(2, -1, "S")

    assert plateau.contains(position) is False


@pytest.fixture
def rover():
    return Rover(Position(1, 2, "N"))


@pytest.fixture
def plateau():
    return Plateau(5, 5)


def test_rover_stores_position(rover):
    assert rover.position.x == 1
    assert rover.position.y == 2
    assert rover.position.direction == "N"


def test_rover_rotates_left(rover):
    rover.rotate("L")

    assert rover.position.direction == "W"
    assert rover.position.x == 1
    assert rover.position.y == 2


def test_rover_rotates_right(rover):
    rover.rotate("R")

    assert rover.position.direction == "E"


def test_rover_moves_forward(rover, plateau):
    rover.move(plateau)

    assert rover.position.x == 1
    assert rover.position.y == 3
    assert rover.position.direction == "N"


def test_rover_refuses_move_outside_plateau():
    rover = Rover(Position(5, 5, "N"))
    plateau = Plateau(5, 5)

    rover.move(plateau)

    assert rover.position.x == 5
    assert rover.position.y == 5


def test_rover_executes_instruction_sequence(rover, plateau):
    instructions = [
        "L", "M", "L", "M", "L",
        "M", "L", "M", "M",
    ]

    result = rover.execute_instructions(
        instructions,
        plateau,
    )

    assert result.x == 1
    assert result.y == 3
    assert result.direction == "N"
