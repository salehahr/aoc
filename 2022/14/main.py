import re

import numpy as np
from Grid import Grid

from tools import parse_lines, print_part


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    rock_paths = [
        [tuple(map(int, m)) for m in re.findall(r"(\d+)\,(\d+)", line)]
        for line in lines
    ]

    grid = Grid(rock_paths, part)
    grid.start(part)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
