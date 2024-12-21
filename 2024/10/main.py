import queue
from typing import Callable

import numpy as np

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, get_neighbours

TRAIL_END = 9


def bfs(start_rc: Coordinates, map_: np.array, next_states: Callable, part: int) -> int:
    """
    Breadth First Search.
    """
    seen = {start_rc}  # seen RCs
    to_explore = queue.LifoQueue()
    to_explore.put(start_rc)

    score = 0

    while not to_explore.empty():
        rc = to_explore.get()

        if map_[rc] == TRAIL_END:
            score += 1
            continue

        neighbours = set(next_states(rc))
        if part == 1:
            neighbours -= seen  # unique paths don't matter

        seen |= neighbours
        for nrc in neighbours:
            to_explore.put(nrc)

    return score


@print_part
def solve(filepath: str, part: int = 1):
    map_ = get_array(filepath, func=int)

    def _neighbours(rc: Coordinates):
        valid_dirs = get_neighbours(rc, *map_.shape)
        return filter(lambda x: map_[x] == (map_[rc] + 1), valid_dirs)

    def score(start_rc: Coordinates) -> int:
        return bfs(start_rc, map_, next_states=_neighbours, part=part)

    start_positions = (Coordinates(*map(int, rc)) for rc in np.argwhere(map_ == 0))
    ans = sum(map(score, start_positions))

    print_ans(ans, correct_ans=789 if part == 1 else 1735)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
