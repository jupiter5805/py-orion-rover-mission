from src.logic import rotate, move, execute_instructions


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


def test_move_north():
    position = {"x": 0, "y": 0, "direction": "N"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 0, "y": 1, "direction": "N"}


def test_move_east():
    position = {"x": 1, "y": 1, "direction": "E"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 2, "y": 1, "direction": "E"}


def test_move_south():
    position = {"x": 1, "y": 1, "direction": "S"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 1, "y": 0, "direction": "S"}


def test_move_west():
    position = {"x": 1, "y": 1, "direction": "W"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 0, "y": 1, "direction": "W"}


def test_move_does_not_go_past_north_edge():
    position = {"x": 2, "y": 5, "direction": "N"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 2, "y": 5, "direction": "N"}


def test_move_does_not_go_past_east_edge():
    position = {"x": 5, "y": 2, "direction": "E"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 5, "y": 2, "direction": "E"}


def test_move_does_not_go_past_south_edge():
    position = {"x": 2, "y": 0, "direction": "S"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 2, "y": 0, "direction": "S"}


def test_move_does_not_go_past_west_edge():
    position = {"x": 0, "y": 2, "direction": "W"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 0, "y": 2, "direction": "W"}


def test_move_can_move_along_north_edge():
    position = {"x": 4, "y": 5, "direction": "E"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 5, "y": 5, "direction": "E"}


def test_move_can_move_to_upper_right_corner():
    position = {"x": 5, "y": 4, "direction": "N"}
    plateau = {"max_x": 5, "max_y": 5}

    result = move(position, plateau)

    assert result == {"x": 5, "y": 5, "direction": "N"}


def test_execute_instructions_with_empty_list():
    position = {"x": 1, "y": 2, "direction": "N"}
    plateau = {"max_x": 5, "max_y": 5}

    result = execute_instructions(position, [], plateau)

    assert result == {"x": 1, "y": 2, "direction": "N"}


def test_execute_instructions_with_single_left_turn():
    position = {"x": 1, "y": 2, "direction": "N"}
    plateau = {"max_x": 5, "max_y": 5}

    result = execute_instructions(position, ["L"], plateau)

    assert result == {"x": 1, "y": 2, "direction": "W"}


def test_execute_instructions_with_single_move():
    position = {"x": 1, "y": 2, "direction": "N"}
    plateau = {"max_x": 5, "max_y": 5}

    result = execute_instructions(position, ["M"], plateau)

    assert result == {"x": 1, "y": 3, "direction": "N"}
