from src.input_layer import parse_mission
from src.logic import run_mission


def test_brief_mission_end_to_end():
    text = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

    mission = parse_mission(text)
    result = run_mission(mission)

    assert result == [
        {"x": 1, "y": 3, "direction": "N"},
        {"x": 5, "y": 1, "direction": "E"},
    ]


def test_different_mission_end_to_end():
    text = """3 3
0 0 N
MMRMM
3 3 S
MLM"""

    mission = parse_mission(text)
    result = run_mission(mission)

    assert result == [
        {"x": 2, "y": 2, "direction": "E"},
        {"x": 3, "y": 2, "direction": "E"},
    ]
