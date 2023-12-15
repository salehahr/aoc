from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from tools import get_array, print_part
from tools.generic_types import Coordinates, Direction

if TYPE_CHECKING:
    import numpy as np


def within_bounds(rc: Coordinates, max_r: int, max_c: int) -> bool:
    if rc.r < 0 or rc.c < 0:
        return False
    if rc.r > max_r or rc.c > max_c:
        return False
    return True


def propagate(
    map_: np.array,
    seen: set,
    hist_starts: set,
    next_starts: deque,
    bounds_check: callable,
):
    rc0, direction = next_starts.popleft()

    new_rc = rc0
    seen.add(new_rc)

    while map_[new_rc] == ".":
        tmp_rc = new_rc + direction
        if bounds_check(tmp_rc):
            new_rc = tmp_rc
            seen.add(new_rc)
        else:
            break

    handle_blocker(map_, new_rc, hist_starts, next_starts, direction)


def handle_blocker(
    map_: np.array,
    blocker: Coordinates,
    hist_starts: set,
    next_starts: deque,
    approach_from: Direction = None,
):
    valid_directions: list[Direction] = []
    height, width = map_.shape

    match blocker_symbol := map_[blocker]:
        case "|":
            if (
                approach_from == Direction.LEFT or approach_from == Direction.RIGHT
            ):  # split
                if blocker.r > 0:
                    valid_directions.append(Direction.UP)
                if blocker.r < height - 1:
                    valid_directions.append(Direction.DOWN)
            else:  # continue
                if approach_from == Direction.UP and blocker.r > 0:
                    valid_directions.append(approach_from)
                elif approach_from == Direction.DOWN and blocker.r < height - 1:
                    valid_directions.append(approach_from)
        case "-":
            if (
                approach_from == Direction.UP or approach_from == Direction.DOWN
            ):  # split
                if blocker.c > 0:
                    valid_directions.append(Direction.LEFT)
                if blocker.c < width - 1:
                    valid_directions.append(Direction.RIGHT)
            else:  # continue
                if approach_from == Direction.LEFT and blocker.c > 0:
                    valid_directions.append(approach_from)
                elif approach_from == Direction.RIGHT and blocker.c < width - 1:
                    valid_directions.append(approach_from)
        case "/" | "\\":
            match (blocker_symbol, approach_from):
                case ("/", Direction.RIGHT) | ("\\", Direction.LEFT):
                    if blocker.r > 0:
                        valid_directions.append(Direction.UP)
                case ("/", Direction.LEFT) | ("\\", Direction.RIGHT):
                    if blocker.r < height - 1:
                        valid_directions.append(Direction.DOWN)
                case ("/", Direction.UP) | ("\\", Direction.DOWN):
                    if blocker.c < width - 1:
                        valid_directions.append(Direction.RIGHT)
                case ("/", Direction.DOWN) | ("\\", Direction.UP):
                    if blocker.c > 0:
                        valid_directions.append(Direction.LEFT)

    next_starts += {
        (blocker + valid_dir, valid_dir) for valid_dir in valid_directions
    } - hist_starts
    hist_starts |= set(next_starts)


def get_num_tiles_seen(
    map_: np.array, start: [Coordinates, Direction], bounds_check: callable
):
    seen = set()
    hist_starts = set()
    next_starts = deque([start])

    while next_starts:
        propagate(map_, seen, hist_starts, next_starts, bounds_check)

    return len(seen)


@print_part
def solve(filepath: str, part: int):
    map_ = get_array(filepath)
    max_r, max_c = Coordinates(*map_.shape) + (-1, -1)

    def __bounds_check(rc: Coordinates):
        return within_bounds(rc, max_r=max_r, max_c=max_c)

    if part == 1:
        starts = {(Coordinates(0, 0), Direction.RIGHT)}
    else:
        sides_tb = {
            (Coordinates(r, c), d)
            for c in range(max_c)
            for (r, d) in [(0, Direction.DOWN), (max_r, Direction.UP)]
        }
        sides_lr = {
            (Coordinates(r, c), d)
            for r in range(0, max_r)
            for (c, d) in [(0, Direction.RIGHT), (max_c, Direction.LEFT)]
        }
        starts = sides_tb | sides_lr

    result = max([get_num_tiles_seen(map_, start, __bounds_check) for start in starts])
    print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
