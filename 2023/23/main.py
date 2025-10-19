import numpy as np

from tools import get_array, print_part
from tools.generic_types import CHAR_TO_DIRECTIONS, Coordinates, Direction


def get_neighbours(rc: Coordinates, map_: np.array):
    for direction in Direction:
        nrc = rc + direction
        if (n_sym := map_[nrc]) in CHAR_TO_DIRECTIONS.keys():
            allowed_direction = CHAR_TO_DIRECTIONS[n_sym]
            if direction == allowed_direction:
                yield nrc
        else:
            yield nrc


@print_part
def solve(filepath: str, part: int):
    map_ = get_array(filepath)
    height, width = map_.shape

    if part == 2:
        for sym in CHAR_TO_DIRECTIONS.keys():
            map_[map_ == sym] = "."

    start_rc = Coordinates(0, 1)
    end_rc = Coordinates(height - 1, width - 2)

    free = {Coordinates(*rc) for rc in np.argwhere(map_ != "#")} - {start_rc}

    paths_to_check = [[start_rc]]
    longest_path = [None]

    while paths_to_check:
        path = paths_to_check.pop()
        rc = path[-1]
        while rc != end_rc:
            neighbours = ({n for n in get_neighbours(rc, map_)} & free) - set(path)
            if len(neighbours) == 0:
                break
            elif len(neighbours) == 1:
                next_rc = neighbours.pop()
                path.append(next_rc)
                rc = next_rc
            else:
                next_rc, *next_neighbours = list(neighbours)
                paths_to_check += [path + [n] for n in next_neighbours]
                path.append(next_rc)
                rc = next_rc

        if len(path) > len(longest_path):
            longest_path = path

    res = len(longest_path) - 1
    print(res)


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
