import logging

from main import run
from src.archive import load_archive


def test_run_handles_invalid_mission_without_crashing(
    capsys,
    tmp_path,
):
    path = tmp_path / "mission.json"

    result = run(
        "5",
        archive_path=path,
    )

    captured = capsys.readouterr()

    assert result == []

    assert (
        "Mission error:"
        in captured.out
    )

    assert (
        "Plateau must contain "
        "two coordinates"
        in captured.out
    )

    assert not path.exists()


def test_run_still_executes_valid_mission(
    capsys,
    tmp_path,
):
    text = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

    path = tmp_path / "mission.json"

    result = run(
        text,
        archive_path=path,
    )

    captured = capsys.readouterr()

    assert result == [
        {
            "x": 1,
            "y": 3,
            "direction": "N",
        },
        {
            "x": 5,
            "y": 1,
            "direction": "E",
        },
    ]

    assert "1 3 N" in captured.out
    assert "5 1 E" in captured.out

    assert (
        f"Archive written to: {path}"
        in captured.out
    )

    assert path.exists()


def test_run_writes_valid_archive(
    tmp_path,
):
    text = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""

    path = tmp_path / "mission.json"

    run(
        text,
        archive_path=path,
    )

    archive = load_archive(path)

    assert archive["plateau"] == {
        "max_x": 5,
        "max_y": 5,
    }

    assert len(
        archive["rovers"]
    ) == 2

    assert archive["rovers"][0] == {
        "type": "standard",
        "starting_position": {
            "x": 1,
            "y": 2,
            "direction": "N",
        },
        "final_position": {
            "x": 1,
            "y": 3,
            "direction": "N",
        },
    }

    assert archive["rovers"][1] == {
        "type": "standard",
        "starting_position": {
            "x": 3,
            "y": 3,
            "direction": "E",
        },
        "final_position": {
            "x": 5,
            "y": 1,
            "direction": "E",
        },
    }

    assert "timestamp" in archive


def test_run_logs_mission_error(
    caplog,
    tmp_path,
):
    path = tmp_path / "mission.json"

    with caplog.at_level(
        logging.ERROR
    ):
        result = run(
            "5",
            archive_path=path,
        )

    assert result == []

    assert (
        "Mission failed"
        in caplog.text
    )
