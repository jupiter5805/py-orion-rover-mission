from src.input_layer import parse_plateau


def test_parse_plateau_returns_dictionary():
    result = parse_plateau("5 5")

    assert result == {"max_x": 5, "max_y": 5}


def test_parse_plateau_works_with_different_size():
    result = parse_plateau("8 10")

    assert result == {"max_x": 8, "max_y": 10}
