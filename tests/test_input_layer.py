from src.input_layer import parse_plateau, parse_position, parse_instructions


def test_parse_plateau_returns_dictionary():
    result = parse_plateau("5 5")

    assert result == {"max_x": 5, "max_y": 5}


def test_parse_plateau_works_with_different_size():
    result = parse_plateau("8 10")

    assert result == {"max_x": 8, "max_y": 10}


def test_parse_position_returns_dictionary():
    result = parse_position("1 2 N")

    assert result == {"x": 1, "y": 2, "direction": "N"}


def test_parse_position_works_with_different_position():
    result = parse_position("3 4 E")

    assert result == {"x": 3, "y": 4, "direction": "E"}


def test_parse_position_can_parse_north():
    result = parse_position("0 0 N")

    assert result == {"x": 0, "y": 0, "direction": "N"}


def test_parse_position_can_parse_east():
    result = parse_position("0 0 E")

    assert result == {"x": 0, "y": 0, "direction": "E"}


def test_parse_position_can_parse_south():
    result = parse_position("0 0 S")

    assert result == {"x": 0, "y": 0, "direction": "S"}


def test_parse_position_can_parse_west():
    result = parse_position("0 0 W")

    assert result == {"x": 0, "y": 0, "direction": "W"}


def test_parse_instructions_returns_list():
    result = parse_instructions("M")

    assert type(result) == list


def test_parse_instructions_single_instruction():
    result = parse_instructions("M")

    assert result == ["M"]


def test_parse_instructions_multiple_instructions_in_order():
    result = parse_instructions("LMLMLMLMM")

    assert result == ["L", "M", "L", "M", "L", "M", "L", "M", "M"]
