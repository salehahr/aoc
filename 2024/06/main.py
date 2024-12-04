import itertools

import numpy as np

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, Direction


class Guard:
    def __init__(self, map_: np.array, direction0: Direction):
        self.pos = Coordinates(*np.argwhere(map_ == "^")[0])
        self.direction = direction0

    def turn(self):
        self.direction = Direction.rotate_90(self.direction, clockwise=True)


@print_part
def solve(filepath: str, part: int = 1):
    map_ = get_array(filepath)
    height, width = map_.shape
    obstacles = tuple(Coordinates(*x) for x in np.argwhere(map_ == "#"))
    guard = Guard(map_, direction0=Direction.UP)

    def _next_obstacle(pos: Coordinates, direction: Direction) -> Coordinates:
        nonlocal obstacles
        if direction.is_vertical:
            if direction == Direction.UP:
                rows_to_check = range(pos.r - 1, -1, -1)
            else:
                rows_to_check = range(pos.r + 1, height + 1)

            for r in rows_to_check:
                if (obstacle := Coordinates(r, pos.c)) in obstacles:
                    return obstacle
        else:
            if direction == Direction.LEFT:
                cols_to_check = range(pos.c - 1, -1, -1)
            else:
                cols_to_check = range(pos.c + 1, width + 1)

            for c in cols_to_check:
                if (obstacle := Coordinates(pos.r, c)) in obstacles:
                    return obstacle

    def _num_next_steps(obstacle: Coordinates | None = None) -> int:
        if obstacle:
            return int((obstacle - guard.pos - guard.direction).magnitude)
        else:
            match guard.direction:
                case Direction.UP:
                    return guard.pos.r
                case Direction.DOWN:
                    return height - 1 - guard.pos.r
                case Direction.LEFT:
                    return guard.pos.c
                case Direction.RIGHT:
                    return width - 1 - guard.pos.c

    visited = []
    next_obj = "#"

    while next_obj:
        next_obj = _next_obstacle(guard.pos, guard.direction)
        num_next_steps = _num_next_steps(next_obj)
        current_path = list(
            itertools.accumulate(
                (guard.direction.value for _ in range(num_next_steps)),
                initial=guard.pos,
            )
        )
        visited.append((guard.direction, current_path))

        guard.pos = current_path[-1]
        guard.turn()

    if part == 1:
        _, paths = zip(*visited)
        unique_visited = set(itertools.chain(*paths))
        print_ans(len(unique_visited), correct_ans=5444)
        return

    has_intersection = 0

    for i, (current_dir, current_path) in enumerate(visited):
        next_dir = Direction.rotate_90(current_dir, clockwise=True)
        possible_next_paths = [v[1] for v in visited[:i] if v[0] == next_dir]

        for possible_next_path in possible_next_paths:
            if next_dir.is_vertical:
                col = possible_next_path[0].c
                has_intersection += any(filter(lambda rc: rc.c == col, current_path))
            else:
                row = possible_next_path[0].r
                has_intersection += any(filter(lambda rc: rc.r == row, current_path))

    print_ans(has_intersection)  # 1069/976 too low


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
