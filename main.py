from src.input_layer import parse_mission
from src.logic import run_mission
from src.exceptions import MissionError


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


def run(text):
    try:
        mission = parse_mission(text)
        final_positions = run_mission(mission)

    except MissionError as error:
        print(f"Mission error: {error}")
        return []

    for position in final_positions:
        print(format_position(position))

    return final_positions


def main():
    return run(INPUT)


if __name__ == "__main__":
    main()
