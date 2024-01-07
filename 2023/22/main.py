from collections import defaultdict
from typing import Optional

import numpy as np
from Brick import Brick
from tools import parse_lines, print_part


def parse_data(filepath: str) -> [list[Brick], np.array, int]:
    lines = list(map(lambda x: x.split("~"), parse_lines(filepath)))
    bricks: list[Optional[Brick]] = [None] * len(lines)

    for b_id, line in enumerate(lines, start=1):
        start, end = map(lambda x: tuple(int(xx) for xx in x.split(",")), line)
        bricks[b_id - 1] = Brick(b_id, *[range(start[i], end[i]) for i in range(0, 3)])
    bricks.sort()

    invalid_id = len(bricks) * 2

    x_range = {v for b in bricks for v in list(range(b.x.start, b.x.stop + 1))}
    y_range = {v for b in bricks for v in list(range(b.y.start, b.y.stop + 1))}
    z_range = {v for b in bricks for v in list(range(b.z.start, b.z.stop + 1))}

    grid = np.full((max(x_range) + 1, max(y_range) + 1, len(z_range) + 1), 0)
    grid[:, :, 0] = invalid_id

    return bricks, grid, invalid_id


def fall(brick: Brick, grid: np.array, invalid_id: int, supports: dict):
    rx, ry = brick.x, brick.y
    blocks_below = grid[
        rx.start : rx.stop + 1, ry.start : ry.stop + 1, : brick.z.start + 1
    ]
    z_occupied = np.any(np.any(blocks_below, axis=0), axis=0)
    z = max(np.where(z_occupied)[0]) + 1

    grid[
        rx.start : rx.stop + 1, ry.start : ry.stop + 1, z : z + brick.height
    ] = brick.id_
    brick.at_rest = True

    if z != brick.z.start:
        brick.z = range(z, z + brick.height - 1)

    supported_by = blocks_below[:, :, z - 1]
    supported_by = set(np.unique(supported_by).tolist()) - {0} - {invalid_id}
    brick.supported_by |= supported_by
    for s in supported_by:
        supports[s] |= {brick.id_}


@print_part
def solve(filepath: str, part: int):
    bricks, grid, invalid_id = parse_data(filepath)
    supports = defaultdict(set)

    for brick in bricks:
        fall(brick, grid, invalid_id, supports)

    # bricks which are the sole supporters of at least one brick above
    single_supports = {
        ss
        for b in filter(lambda b: len(b.supported_by) <= 1, bricks)
        for ss in b.supported_by
    }

    if part == 1:
        return len(bricks) - len(single_supports)
    else:
        bricks.sort(key=lambda x: x.id_)
        num_chain = 0
        for ss in single_supports:
            removed, to_do = set(), {ss}

            while to_do:
                brick = to_do.pop()
                prev_bricks = bricks[brick - 1].supported_by

                # s can still be supported by another brick not in single_supports
                if removed and not prev_bricks.issubset(removed):
                    continue

                removed.add(brick)
                to_do |= supports[brick]

            num_chain += len(removed) - 1

        return num_chain


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
