class MissionError(Exception):
    """Base exception for all mission-related errors."""


class InvalidPlateauError(MissionError):
    """Raised when plateau input is invalid."""


class InvalidPositionError(MissionError):
    """Raised when a rover position is invalid."""


class InvalidInstructionError(MissionError):
    """Raised when rover instructions are invalid."""


class InvalidMissionError(MissionError):
    """Raised when the overall mission structure is invalid."""
