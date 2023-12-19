from functools import lru_cache

import numpy as np
from tools import get_array, print_part
from tools.generic_types import Coordinates, Direction, get_neighbours


@print_part
def solve(filepath: str, part: int):
    garden = get_array(filepath)
    height, width = garden.shape

    start_rc = Coordinates(*np.argwhere(garden == "S")[0])
    rocks = {Coordinates(*c) for c in np.argwhere(garden == "#")}

    to_explore = {start_rc}
    num_steps = 64 if part == 1 else 26501365

    @lru_cache
    def __get_neighbours(rc: Coordinates, part):
        if part == 1:
            return {
                nrc for nrc in get_neighbours(rc, height, width) if nrc not in rocks
            }
        else:
            return {rc + direction for direction in Direction} - rocks

    for x in range(1, num_steps + 1):
        n = set()

        while to_explore:
            rc = to_explore.pop()
            if part == 1:
                n |= __get_neighbours(rc, part)
            else:
                n |= __get_neighbours(Coordinates(rc.r % height, rc.c % width), part)
        to_explore |= n

        if x in [1, 2, 4, 5, 6, 7, 8, 9, 10, 16, 25, 27, 30, 50, 100, 500, 1000, 5000]:
            print(f"{x=}, {len(to_explore)=}")
    print(f"{x=}, {len(to_explore)=}")

    # garden[garden == "."] = " "
    # for rc in to_explore:
    #     garden[rc] = "O"
    # for line in garden:
    #     print(line)


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
