from enum import Enum
from typing import Iterable

import numpy as np

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, Direction, in_bounds


class WsDirection(Enum):
    EAST = Direction.RIGHT.value
    SOUTH = Direction.DOWN.value
    WEST = Direction.LEFT.value
    NORTH = Direction.UP.value
    NORTH_WEST = Coordinates(1, 1)
    NORTH_EAST = Coordinates(1, -1)
    SOUTH_WEST = Coordinates(-1, -1)
    SOUTH_EAST = Coordinates(-1, 1)


@print_part
def solve(filepath: str, part: int = 1):
    arr = get_array(filepath)

    def _in_bounds(coords: Coordinates) -> bool:
        return in_bounds(coords, *arr.shape)

    def _matches_term(
        term: str,
        ref_rc: Coordinates,
        direction_: WsDirection,
        relative_positions: Iterable[int],
    ):
        dir_coords = (ref_rc + (i * direction_.value) for i in relative_positions)
        dir_coords = filter(_in_bounds, dir_coords)
        return "".join(arr[x, y] for x, y in dir_coords) == term

    if part == 1:

        def _matches_xmas(x_rc: Coordinates, direction_: WsDirection) -> bool:
            return _matches_term(
                "XMAS", ref_rc=x_rc, direction_=direction_, relative_positions=range(4)
            )

        x_rcs = (Coordinates(r, c) for r, c in zip(*np.where(arr == "X")))
        ans = sum(
            _matches_xmas(x_rc, direction_=d) for x_rc in x_rcs for d in WsDirection
        )
        print_ans(ans, correct_ans=2530)
    else:

        def _matches_mas(a_rc: Coordinates, direction_: WsDirection) -> bool:
            return _matches_term(
                "MAS",
                ref_rc=a_rc,
                direction_=direction_,
                relative_positions=range(-1, 2),
            )

        a_rcs = (Coordinates(r, c) for r, c in zip(*np.where(arr == "A")))
        diags = {d for d in WsDirection if "_" in d.name}
        a_diags = {
            a_rc: {d for d in diags if _matches_mas(a_rc, direction_=d)}
            for a_rc in a_rcs
        }
        ans = sum(1 for d in a_diags.values() if len(d) > 1)
        print_ans(ans, correct_ans=1921)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
