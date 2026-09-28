from src.input_layer import parse_mission
from src.logic import run_mission


INPUT = """5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM"""


def main():
    mission = parse_mission(INPUT)
    final_positions = run_mission(mission)

    for position in final_positions:
        print(
            f'{position["x"]} '
            f'{position["y"]} '
            f'{position["direction"]}'
        )


if __name__ == "__main__":
    main()
