from src.models import Position
from src.models import Position, Plateau


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
