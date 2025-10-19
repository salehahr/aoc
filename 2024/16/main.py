from queue import LifoQueue
from typing import Iterable

import numpy as np

from tools import get_array, manhattan_distance, print_ans, print_part
from tools.generic_types import BaseState, Coordinates, Direction, get_neighbours
from tools.pathfinding import dijkstra, multipath_dijkstra


class State(BaseState):
    rc: Coordinates
    dir_: Direction


def dfs(xn: Iterable[State], prev_states: dict[State, set[State]]):
    to_explore = LifoQueue()
    for st in xn:
        to_explore.put(st)
    seen = set()
    while not to_explore.empty():
        st = to_explore.get()
        seen.add(st.rc)
        if prevs := prev_states[st]:
            for prev in prevs:
                to_explore.put(prev)
    return seen


@print_part
def solve(filepath: str, part: int = 1):
    map_ = get_array(filepath)

    start_pos = Coordinates(*np.argwhere(map_ == "S")[0])
    end_pos = Coordinates(*np.argwhere(map_ == "E")[0])
    walls = {Coordinates(*xy) for xy in np.argwhere(map_ == "#")}
    start_dir = Direction.RIGHT

    def __next_coords(x: State) -> set[State]:
        neighbours = set(get_neighbours(x.rc, *map_.shape)) - walls
        return {State(n, Direction(n - x.rc)) for n in neighbours}

    def __score(x: State, x_next: State) -> int:
        """Penalise high scores."""
        if x.dir_.category == x_next.dir_.category:
            if x.dir_ == x_next.dir_:
                score_ = 1
            else:
                score_ = 2 * 1000 + 1
        else:
            score_ = 1000 + 1
        return score_

    def __break(x: State) -> bool:
        return x.rc == end_pos

    def __heuristic(x: State) -> int:
        """Penalise distance to end_pos"""
        return manhattan_distance(*end_pos, *x.rc)

    x0 = {State(start_pos, start_dir)}

    if part == 1:
        ans, path = dijkstra(
            x0,
            next_states=__next_coords,
            transition_cost=__score,
            break_condition=__break,
        )
    else:
        scores, prev_states = multipath_dijkstra(
            x0,
            next_states=__next_coords,
            transition_cost=__score,
            break_condition=__break,
            heuristic=__heuristic,
        )

        final_scores, x_end = zip(
            *((score, st) for st, score in scores.items() if st.rc == end_pos)
        )
        best_score = min(final_scores)
        best_x_end = (
            st for score, st in zip(final_scores, x_end) if score == best_score
        )
        seen = dfs(best_x_end, prev_states)
        ans = len(seen)

    print_ans(ans, correct_ans=147628 if part == 1 else 670)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
