import logging
from datetime import datetime, timezone
from pathlib import Path

from src.archive import build_archive, save_archive
from src.exceptions import MissionError
from src.input_layer import (
    parse_instructions,
    parse_plateau,
    parse_position,
)
from src.logic import run_mission


logger = logging.getLogger(__name__)


def format_position(position):
    return (
        f'{position["x"]} '
        f'{position["y"]} '
        f'{position["direction"]}'
    )


def create_archive_path():
    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")

    return (
        Path("archives")
        / f"mission_{timestamp}.json"
    )


def execute_mission(
    mission,
    archive_path=None,
):
    logger.info("Starting mission")

    try:
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

    print("\nMission complete.")

    for index, position in enumerate(
        final_positions,
        start=1,
    ):
        print(
            f"Rover {index}: "
            f"{format_position(position)}"
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
        f"Archive written to: "
        f"{saved_path}"
    )

    return final_positions


def run(
    text,
    archive_path=None,
):
    from src.input_layer import parse_mission

    try:
        mission = parse_mission(text)

    except MissionError as error:
        logger.error(
            "Mission failed: %s",
            error,
        )

        print(
            f"Mission error: {error}"
        )

        return []

    return execute_mission(
        mission,
        archive_path=archive_path,
    )


def prompt_for_plateau(input_func=input):
    while True:
        text = input_func(
            "Enter plateau size "
            "(e.g. 5 5): "
        )

        try:
            return parse_plateau(text)

        except MissionError as error:
            print(
                f"Invalid plateau: {error}"
            )


def prompt_for_position(input_func=input):
    while True:
        text = input_func(
            "Enter rover position "
            "(e.g. 1 2 N, or 1 2 N C "
            "for cargo): "
        )

        try:
            return parse_position(text)

        except MissionError as error:
            print(
                f"Invalid position: {error}"
            )


def prompt_for_instructions(
    input_func=input,
):
    while True:
        text = input_func(
            "Enter rover instructions "
            "(L, R, M): "
        )

        try:
            return parse_instructions(text)

        except MissionError as error:
            print(
                f"Invalid instructions: "
                f"{error}"
            )


def prompt_add_another(
    input_func=input,
):
    while True:
        answer = input_func(
            "Add another rover? "
            "(y/n): "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print(
            "Please enter y or n."
        )


def interactive_session(
    input_func=input,
    archive_path=None,
):
    print(
        "=== ORION 7 MISSION CONTROL ==="
    )

    plateau = prompt_for_plateau(
        input_func
    )

    rovers = []

    while True:
        print(
            f"\nRover {len(rovers) + 1}"
        )

        position = (
            prompt_for_position(
                input_func
            )
        )

        instructions = (
            prompt_for_instructions(
                input_func
            )
        )

        rovers.append(
            {
                "position": position,
                "instructions": instructions,
            }
        )

        if not prompt_add_another(
            input_func
        ):
            break

    mission = {
        "plateau": plateau,
        "rovers": rovers,
    }

    return execute_mission(
        mission,
        archive_path=archive_path,
    )


def main():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(levelname)s:"
            "%(name)s:"
            "%(message)s"
        ),
    )

    interactive_session()


if __name__ == "__main__":
    main()
