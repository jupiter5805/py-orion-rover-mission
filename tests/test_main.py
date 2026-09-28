from main import run


def test_run_handles_invalid_mission_without_crashing(capsys):
    result = run("5")

    captured = capsys.readouterr()

    assert result == []
    assert "Mission error:" in captured.out
    assert "Plateau must contain two coordinates" in captured.out


def test_run_still_executes_valid_mission(capsys):
    text = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

    result = run(text)

    captured = capsys.readouterr()

    assert result == [
        {"x": 1, "y": 3, "direction": "N"},
        {"x": 5, "y": 1, "direction": "E"},
    ]

    assert captured.out == "1 3 N\n5 1 E\n"
