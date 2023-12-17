from __future__ import annotations

import sys
from collections import defaultdict
from queue import PriorityQueue, Queue
from typing import TYPE_CHECKING, Callable, Iterable

if TYPE_CHECKING:
    from tools.generic_types import BaseState, Coordinates

    NumericType = int | float


"""
https://www.redblobgames.com/pathfinding/a-star/introduction.html
"""


def get_path(xn: BaseState, prev_rc: dict[BaseState, BaseState]):
    rc, path = xn, []

    while rc in prev_rc:
        path.append(rc)
        rc = prev_rc[rc]

    path.reverse()

    return path


def bfs(start_rc: Coordinates, end_rc: Coordinates, next_states: Callable):
    """
    Breadth First Search.
    """
    prev_rc = {start_rc: None}  # keys: already seen RCs
    to_explore = Queue()
    to_explore.put(start_rc)

    while not to_explore.empty():
        rc = to_explore.get()

        if rc == end_rc:
            get_path(end_rc, prev_rc)
            break

        neighbours = set(next_states(rc)) - set(prev_rc.keys())
        for nrc in neighbours:
            to_explore.put(nrc)
            prev_rc[nrc] = rc


def dijkstra(
    x0: Iterable[BaseState],
    next_states: Callable[[BaseState], Iterable[BaseState]],
    transition_cost: Callable[[BaseState, BaseState], NumericType],
    break_condition: Callable[[BaseState], bool],
    heuristic: Callable[[BaseState], NumericType] = lambda x: 0,
):
    prev_rc = {}
    running_costs = defaultdict(lambda: sys.maxsize)
    to_explore = PriorityQueue()

    for x in x0:
        prev_rc[x] = None
        running_costs[x] = 0
        to_explore.put((0, x))

    while not to_explore.empty():
        _, x = to_explore.get()

        if break_condition(x):
            return running_costs[x], get_path(x, prev_rc)

        for x_next in next_states(x):
            cost = running_costs[x] + transition_cost(x, x_next)
            if cost < running_costs[x_next]:
                running_costs[x_next] = cost
                priority = cost + heuristic(x_next)
                to_explore.put((priority, x_next))
                prev_rc[x_next] = x
