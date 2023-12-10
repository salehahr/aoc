import itertools

import numpy as np
from tools import manhattan_distance, parse_lines, print_part

Coordinates = tuple[int, int]


def expand(
    galaxy_map: np.array,
    replace_empty_by: int,
) -> list[Coordinates]:
    galaxies = [rc for rc in zip(*np.where(galaxy_map == "#"))]

    empty_rows = np.where(np.all(galaxy_map == "", axis=1))
    empty_cols = np.where(np.all(galaxy_map == "", axis=0))

    for i, (row, col) in enumerate(galaxies):
        new_row = row + (replace_empty_by - 1) * sum(sum(empty_rows < row))
        new_col = col + (replace_empty_by - 1) * sum(sum(empty_cols < col))
        galaxies[i] = (new_row, new_col)

    return galaxies


@print_part
def solve(filepath: str, part: int):
    galaxy_map = np.array(
        [[c if c == "#" else "" for c in line] for line in parse_lines(filepath)]
    )
    galaxies = expand(galaxy_map, replace_empty_by=2 if part == 1 else 1000000)
    combinations = itertools.combinations(range(len(galaxies)), r=2)
    distance = sum(
        [manhattan_distance(*galaxies[g1], *galaxies[g2]) for g1, g2 in combinations]
    )
    print(distance)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
