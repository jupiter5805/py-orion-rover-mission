import logging
from datetime import datetime, timezone
from pathlib import Path

from src.input_layer import parse_mission
from src.logic import run_mission
from src.exceptions import MissionError
from src.archive import (
    build_archive,
    save_archive,
)


logger = logging.getLogger(__name__)


INPUT = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""


def format_position(position):
    return (
        f'{position["x"]} '
        f'{position["y"]} '
        f'{position["direction"]}'
    )


def create_archive_path():
    timestamp = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    return (
        Path("archives")
        / f"mission_{timestamp}.json"
    )


def run(
    text,
    archive_path=None,
):
    logger.info(
        "Starting mission"
    )

    try:
        mission = parse_mission(text)

        final_positions = run_mission(
            mission
        )

    except MissionError as error:
        logger.error(
            "Mission failed: %s",
            error,
        )

        print(
            f"Mission error: {error}"
        )

        return []

    logger.info(
        "Mission completed with %s rover(s)",
        len(final_positions),
    )

    for position in final_positions:
        print(
            format_position(position)
        )

    archive = build_archive(
        mission,
        final_positions,
    )

    if archive_path is None:
        archive_path = (
            create_archive_path()
        )

    saved_path = save_archive(
        archive,
        archive_path,
    )

    print(
        f"Archive written to: {saved_path}"
    )

    return final_positions


def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(levelname)s:"
            "%(name)s:"
            "%(message)s"
        ),
    )

    return run(INPUT)


if __name__ == "__main__":
    main()
