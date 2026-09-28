from src.logic import rotate


def test_rotate_left_from_north():
    position = {"x": 0, "y": 0, "direction": "N"}

    result = rotate(position, "L")

    assert result == {"x": 0, "y": 0, "direction": "W"}


def test_rotate_left_from_west():
    position = {"x": 0, "y": 0, "direction": "W"}

    result = rotate(position, "L")

    assert result == {"x": 0, "y": 0, "direction": "S"}


def test_rotate_left_from_south():
    position = {"x": 0, "y": 0, "direction": "S"}

    result = rotate(position, "L")

    assert result == {"x": 0, "y": 0, "direction": "E"}


def test_rotate_left_from_east():
    position = {"x": 0, "y": 0, "direction": "E"}

    result = rotate(position, "L")

    assert result == {"x": 0, "y": 0, "direction": "N"}


def test_rotate_right_from_north():
    position = {"x": 0, "y": 0, "direction": "N"}

    result = rotate(position, "R")

    assert result == {"x": 0, "y": 0, "direction": "E"}


def test_rotate_right_from_east():
    position = {"x": 0, "y": 0, "direction": "E"}

    result = rotate(position, "R")

    assert result == {"x": 0, "y": 0, "direction": "S"}


def test_rotate_right_from_south():
    position = {"x": 0, "y": 0, "direction": "S"}

    result = rotate(position, "R")

    assert result == {"x": 0, "y": 0, "direction": "W"}


def test_rotate_right_from_west():
    position = {"x": 0, "y": 0, "direction": "W"}

    result = rotate(position, "R")

    assert result == {"x": 0, "y": 0, "direction": "N"}


def test_rotate_does_not_mutate_original_position():
    position = {"x": 1, "y": 2, "direction": "N"}

    result = rotate(position, "R")

    assert position == {"x": 1, "y": 2, "direction": "N"}
    assert result == {"x": 1, "y": 2, "direction": "E"}
    assert result is not position
