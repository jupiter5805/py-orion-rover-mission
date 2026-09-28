from src.archive import (
    build_archive,
    save_archive,
    load_archive,
)


def test_build_archive_contains_mission_outcome():
    mission = {
        "plateau": {
            "max_x": 5,
            "max_y": 5,
        },
        "rovers": [
            {
                "position": {
                    "x": 1,
                    "y": 2,
                    "direction": "N",
                },
                "instructions": [
                    "L",
                    "M",
                ],
            },
            {
                "position": {
                    "x": 1,
                    "y": 1,
                    "direction": "E",
                    "rover_type": "cargo",
                },
                "instructions": [
                    "M",
                ],
            },
        ],
    }

    final_positions = [
        {
            "x": 0,
            "y": 2,
            "direction": "W",
        },
        {
            "x": 3,
            "y": 1,
            "direction": "E",
        },
    ]

    timestamp = "2026-09-28T14:00:00+00:00"

    result = build_archive(
        mission,
        final_positions,
        timestamp=timestamp,
    )

    assert result == {
        "plateau": {
            "max_x": 5,
            "max_y": 5,
        },
        "rovers": [
            {
                "type": "standard",
                "starting_position": {
                    "x": 1,
                    "y": 2,
                    "direction": "N",
                },
                "final_position": {
                    "x": 0,
                    "y": 2,
                    "direction": "W",
                },
            },
            {
                "type": "cargo",
                "starting_position": {
                    "x": 1,
                    "y": 1,
                    "direction": "E",
                },
                "final_position": {
                    "x": 3,
                    "y": 1,
                    "direction": "E",
                },
            },
        ],
        "timestamp": timestamp,
    }


def test_archive_round_trip_is_lossless(
    tmp_path,
):
    archive = {
        "plateau": {
            "max_x": 5,
            "max_y": 5,
        },
        "rovers": [
            {
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
        ],
        "timestamp": (
            "2026-09-28T14:00:00+00:00"
        ),
    }

    path = tmp_path / "mission.json"

    save_archive(
        archive,
        path,
    )

    loaded_archive = load_archive(path)

    assert loaded_archive == archive


def test_save_archive_creates_parent_directory(
    tmp_path,
):
    archive = {
        "plateau": {
            "max_x": 5,
            "max_y": 5,
        },
        "rovers": [],
        "timestamp": (
            "2026-09-28T14:00:00+00:00"
        ),
    }

    path = (
        tmp_path
        / "archives"
        / "mission.json"
    )

    save_archive(
        archive,
        path,
    )

    assert path.exists()
