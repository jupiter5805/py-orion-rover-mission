from src.exceptions import (
    MissionError,
    InvalidPlateauError,
    InvalidPositionError,
    InvalidInstructionError,
    InvalidMissionError,
)


def test_invalid_plateau_error_is_mission_error():
    assert issubclass(InvalidPlateauError, MissionError)


def test_invalid_position_error_is_mission_error():
    assert issubclass(InvalidPositionError, MissionError)


def test_invalid_instruction_error_is_mission_error():
    assert issubclass(InvalidInstructionError, MissionError)


def test_invalid_mission_error_is_mission_error():
    assert issubclass(InvalidMissionError, MissionError)


def test_exception_keeps_useful_message():
    error = InvalidInstructionError("Unknown instruction: 'Q'")

    assert str(error) == "Unknown instruction: 'Q'"
