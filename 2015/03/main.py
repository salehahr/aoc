from itertools import accumulate

from tools import parse_lines, print_ans, print_part

MOVE_MAP = {">": 1 + 0j, "<": -1 + 0j, "^": 0 + 1j, "v": 0 - 1j}
START = 0 + 0j


@print_part
def solve(filepath: str, part: int = 1):
    commands = parse_lines(filepath)[0]
    commands_set = [commands] if part == 1 else [commands[::2], commands[1::2]]
    houses = set().union(
        *[
            set(accumulate([START] + [MOVE_MAP[c] for c in commands]))
            for commands in commands_set
        ]
    )
    print_ans(len(houses))


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
