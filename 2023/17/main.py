from __future__ import annotations

from functools import cache
from typing import Iterable

import numpy as np
from tools import get_array, manhattan_distance, pathfinding, print_part
from tools.generic_types import BaseState, Coordinates, Direction, DirectionCategory


class State(BaseState):
    rc: Coordinates
    dc: DirectionCategory


@print_part
def solve(filepath: str, part: int):
    map_ = get_array(filepath, func=int)
    height, width = map_.shape

    start_rc, end_rc = Coordinates(0, 0), Coordinates(height - 1, width - 1)
    available = {Coordinates(*rc) for rc in np.argwhere(map_)}

    min_moves = 1 if part == 1 else 4
    max_moves = 3 if part == 1 else 10

    def propagate_fcn(x: State) -> Iterable[State]:
        """
        Gets the next state from the current state.
        """
        orthogonal_nodes = {
            State(x.rc + i * direction.value, x.dc.opposite)
            for direction in x.dc.opposite.value
            for i in range(min_moves, max_moves + 1)
        }
        return filter(lambda x: x.rc in available, orthogonal_nodes)

    @cache
    def cost_fcn(x: State, x_next: State) -> int:
        """
        Transition cost for a straight line path fron rc to next_rc.
        """
        diff = x_next.rc - x.rc
        direction = Direction.from_coords(diff)
        chain = [x.rc + i * direction.value for i in range(1, int(diff.magnitude) + 1)]
        return sum([map_[c] for c in chain])

    def break_condition(x: State) -> bool:
        return x.rc == end_rc

    @cache
    def heuristic(x_next: State) -> int:
        return manhattan_distance(*x_next.rc, *end_rc)

    x0 = [
        State(start_rc, DirectionCategory.VERTICAL),
        State(start_rc, DirectionCategory.HORIZONTAL),
    ]
    cost, _ = pathfinding.dijkstra(
        x0, propagate_fcn, cost_fcn, break_condition, heuristic
    )
    print(cost)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
