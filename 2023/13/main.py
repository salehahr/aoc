from typing import Callable

import numpy as np
from tools import parse_lines, print_part


def get_mirror_axis(
    map_: np.array, check: str, is_mirror: Callable[[np.array, np.array], bool]
) -> int:
    height, width = map_.shape
    max_length = width if check == "col" else height
    prev_, next_ = None, None

    for x in range(1, max_length):
        length = min(x, max_length - x)

        match check:
            case "col":
                prev_ = map_[:, x - length : x]
                next_ = np.flip(map_[:, x : x + length], axis=1)
            case "row":
                prev_ = map_[x - length : x, :]
                next_ = np.flip(map_[x : x + length, :], axis=0)

        if is_mirror(prev_, next_):
            return x

    return 0


def mirror_condition(prev_rows: np.array, next_rows: np.array, part: int) -> bool:
    row_comp = prev_rows == next_rows
    if part == 1:
        return np.all(row_comp)
    else:
        num_different_elements = np.size(row_comp) - np.count_nonzero(row_comp)
        return 1 == num_different_elements


@print_part
def solve(filepath: str, part: int):
    def __mirror_condition(*args):
        return mirror_condition(*args, part=part)

    lines = [[c for c in line] for line in parse_lines(filepath)]
    partitions = [-1] + [id_ for id_, line in enumerate(lines) if not line] + [None]
    partition_indices = [
        (partitions[x] + 1, partitions[x + 1]) for x in range(len(partitions) - 1)
    ]

    res = 0
    for p0, p1 in partition_indices:
        mirror = np.array(lines[p0:p1])
        refl_axis = {
            check: get_mirror_axis(mirror, check, __mirror_condition)
            for check in ["col", "row"]
        }
        res += refl_axis["col"] + refl_axis["row"] * 100
    print(res)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
