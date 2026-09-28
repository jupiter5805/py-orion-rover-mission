from src.models import Position


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
