from typing import Callable, Generator, Iterable

import numpy as np

from tools import flatten, get_array, print_ans, print_part
from tools.generic_types import Coordinates, in_bounds


def get_antinodes(
    current_rc: Coordinates,
    neighbour: Coordinates,
    part: int,
    in_bound_fcn: Callable = None,
) -> Iterable[Coordinates]:
    dist = neighbour - current_rc
    if part == 1:
        an_before = current_rc - dist
        an_after = current_rc + 2 * dist
        return filter(in_bound_fcn, (an_before, an_after))
    else:

        def _infinite_antinodes(prev: bool) -> Generator[Coordinates, None, None]:
            next_an = current_rc
            while in_bound_fcn(next_an):
                yield next_an
                if prev:
                    next_an -= dist
                else:
                    next_an += dist

        infinite_antinodes = set(_infinite_antinodes(prev) for prev in (True, False))
        return set().union(*infinite_antinodes)


@print_part
def solve(filepath: str, part: int = 1):
    map_ = get_array(filepath)
    antennae = {Coordinates(*rc): map_[*rc] for rc in np.argwhere(map_ != ".")}
    antennae_groups = {
        v: {k for k, vv in antennae.items() if vv == v} for v in antennae.values()
    }

    def _get_antinodes(rc: Coordinates, neighb: Coordinates) -> Iterable[Coordinates]:
        return get_antinodes(rc, neighb, part, lambda x: in_bounds(x, *map_.shape))

    antinodes = set()
    for group in antennae_groups.values():
        while len(group) > 1:
            coord = group.pop()
            neighbours = group - {coord}
            antinodes |= set(
                flatten(map(lambda n: _get_antinodes(coord, n), neighbours))
            )

    print_ans(len(antinodes), correct_ans=256 if part == 1 else 1005)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
