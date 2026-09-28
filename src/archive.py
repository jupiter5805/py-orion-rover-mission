import json
from datetime import datetime, timezone
from pathlib import Path


def build_archive(
    mission,
    final_positions,
    timestamp=None,
):
    if timestamp is None:
        timestamp = datetime.now(
            timezone.utc
        ).isoformat()

    rover_outcomes = []

    for rover_data, final_position in zip(
        mission["rovers"],
        final_positions,
    ):
        starting_data = rover_data["position"]

        starting_position = {
            "x": starting_data["x"],
            "y": starting_data["y"],
            "direction": starting_data["direction"],
        }

        rover_type = starting_data.get(
            "rover_type",
            "standard",
        )

        rover_outcomes.append(
            {
                "type": rover_type,
                "starting_position": starting_position,
                "final_position": final_position.copy(),
            }
        )

    return {
        "plateau": mission["plateau"].copy(),
        "rovers": rover_outcomes,
        "timestamp": timestamp,
    }


def save_archive(archive, path):
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            archive,
            file,
            indent=2,
        )

    return path


def load_archive(path):
    path = Path(path)

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)
