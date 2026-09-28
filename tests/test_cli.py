from main import interactive_session
from src.archive import load_archive


def make_input(values):
    answers = iter(values)

    return lambda prompt="": next(
        answers
    )


def test_cli_runs_single_rover_mission(
    tmp_path,
    capsys,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "5 5",
            "1 2 N",
            "LMLMLMLMM",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

    captured = capsys.readouterr()

    assert result == [
        {
            "x": 1,
            "y": 3,
            "direction": "N",
        }
    ]

    assert (
        "Mission complete."
        in captured.out
    )

    assert (
        "Rover 1: 1 3 N"
        in captured.out
    )

    assert archive_path.exists()


def test_cli_runs_two_rover_mission(
    tmp_path,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "5 5",
            "1 2 N",
            "LMLMLMLMM",
            "y",
            "3 3 E",
            "MMRMMRMRRM",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

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


def test_cli_supports_cargo_rover(
    tmp_path,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "5 5",
            "1 1 E C",
            "MM",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

    assert result == [
        {
            "x": 5,
            "y": 1,
            "direction": "E",
        }
    ]

    archive = load_archive(
        archive_path
    )

    assert (
        archive["rovers"][0]["type"]
        == "cargo"
    )


def test_cli_reprompts_invalid_plateau(
    tmp_path,
    capsys,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "wrong",
            "5 5",
            "1 2 N",
            "M",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

    captured = capsys.readouterr()

    assert (
        "Invalid plateau:"
        in captured.out
    )

    assert result == [
        {
            "x": 1,
            "y": 3,
            "direction": "N",
        }
    ]


def test_cli_reprompts_invalid_position(
    tmp_path,
    capsys,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "5 5",
            "1 2 Q",
            "1 2 N",
            "M",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

    captured = capsys.readouterr()

    assert (
        "Invalid position:"
        in captured.out
    )

    assert result == [
        {
            "x": 1,
            "y": 3,
            "direction": "N",
        }
    ]


def test_cli_reprompts_invalid_instructions(
    tmp_path,
    capsys,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "5 5",
            "1 2 N",
            "LMQ",
            "M",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

    captured = capsys.readouterr()

    assert (
        "Invalid instructions:"
        in captured.out
    )

    assert result == [
        {
            "x": 1,
            "y": 3,
            "direction": "N",
        }
    ]


def test_cli_reprompts_invalid_yes_no_answer(
    tmp_path,
    capsys,
):
    archive_path = (
        tmp_path / "mission.json"
    )

    input_func = make_input(
        [
            "5 5",
            "1 2 N",
            "M",
            "maybe",
            "n",
        ]
    )

    result = interactive_session(
        input_func=input_func,
        archive_path=archive_path,
    )

    captured = capsys.readouterr()

    assert (
        "Please enter y or n."
        in captured.out
    )

    assert result == [
        {
            "x": 1,
            "y": 3,
            "direction": "N",
        }
    ]
