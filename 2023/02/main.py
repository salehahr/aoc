import math
import re

from tools import parse_lines, print_part

RgbTuple = tuple[str, str, str]

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14
MAX_VALS = (MAX_RED, MAX_GREEN, MAX_BLUE)


def is_possible(game_rgb_matches: list[RgbTuple]) -> bool:
    """
    Returns True if all RGB matches of the game are within the respective maximum values.
    """
    for colour_vals in zip(MAX_VALS, *game_rgb_matches):
        max_val = colour_vals[0]
        colour_possible = all([int(val) <= max_val for val in colour_vals[1:] if val])
        if not colour_possible:
            return False
    return True


def get_min_cube(game_rgb_matches: list[RgbTuple]) -> int:
    """
    Returns the cube of the maximum RGB value observed (minimum RGB value needed) for the game.
    """
    min_val = [0] * 3
    for i, colour_vals in enumerate(zip(*game_rgb_matches)):
        min_val[i] = max([int(val) for val in colour_vals if val])
    return math.prod(min_val)


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    games = [re.findall(r"(\d+) red|(\d+) green|(\d+) blue", line) for line in lines]
    if part == 1:
        results = [id_ for id_, game in enumerate(games, start=1) if is_possible(game)]
    else:
        results = [get_min_cube(game) for game in games]
    print(sum(results))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
