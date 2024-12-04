from enum import Enum

import numpy as np

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, Direction


class WsDirection(Enum):
    HORIZONTAL = [Direction.RIGHT.value * i for i in range(1, 4)]
    VERTICAL = [Direction.DOWN.value * i for i in range(1, 4)]
    HORIZONTAL_BWD = [Direction.LEFT.value * i for i in range(1, 4)]
    VERTICAL_BWD = [Direction.UP.value * i for i in range(1, 4)]
    DIAG_NW = [Coordinates(i, i) for i in range(1, 4)]
    DIAG_NE = [Coordinates(i, -i) for i in range(1, 4)]
    DIAG_SE = [Coordinates(-i, -i) for i in range(1, 4)]
    DIAG_SW = [Coordinates(-i, i) for i in range(1, 4)]


@print_part
def solve(filepath: str, part: int = 1):
    arr: np.array = get_array(filepath)
    ncols = len(arr)
    nrows = np.size(arr) // ncols

    def _in_bounds(coords: Coordinates) -> bool:
        in_row = 0 <= coords.r <= (nrows - 1)
        in_col = 0 <= coords.c <= (ncols - 1)
        return in_row and in_col

    x_rcs = (Coordinates(r, c) for r, c in zip(*np.where(arr == "X")))
    ct = 0
    for orig_rc in x_rcs:
        for direction in WsDirection:
            new_rcs = filter(_in_bounds, (orig_rc + d for d in direction.value))
            ct += "".join(arr[x, y] for x, y in new_rcs) == "MAS"
    if part == 1:
        print(ct)

    m_rcs = (Coordinates(r, c) for r, c in zip(*np.where(arr == "M")))
    diags = {d for d in WsDirection if "DIAG" in d.name}
    ct = 0
    for orig_rc in m_rcs:
        for direction in diags:
            ct += is_mas(orig_rc, direction, arr, _in_bounds)
    if part == 2:
        print(ct)


def is_mas(start_rc: Coordinates, direction, arr, _in_bounds):
    new_rcs = filter(_in_bounds, (start_rc + d for d in direction.value[:-1]))
    return "".join(arr[x, y] for x, y in new_rcs) == "AS"


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    # FILEPATH = "input_sar.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
