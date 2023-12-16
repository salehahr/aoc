import numpy as np
from tools import get_array, print_part
from tools.generic_types import Coordinates, get_neighbours


def can_climb(src: int, dst: int) -> bool:
    return dst <= (src + 1)


def dijkstra(array: np.array, start_rc: Coordinates, end_rc: Coordinates):
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode

    dist_array = np.full(array.shape, np.inf)
    dist_array[start_rc] = 0

    height, width = array.shape
    Q = [Coordinates(r, c) for r in range(height) for c in range(width)]
    Q.sort(key=lambda x: dist_array[x])

    result = None
    while end_rc in Q:
        rc_u = Q.pop(0)

        neighbour_rcs = [
            v
            for v in get_neighbours(rc_u, *array.shape)
            if v in Q and can_climb(array[rc_u], array[v])
        ]

        for v_rc in neighbour_rcs:
            cost = dist_array[rc_u] + 1
            if cost < dist_array[v_rc]:
                dist_array[v_rc] = cost

        Q.sort(key=lambda x: dist_array[x])

    try:
        result = int(dist_array[end_rc][0])
    except OverflowError:
        result = np.inf
    finally:
        return result


@print_part
def solve(filepath: str, part: int = 1):
    array = get_array(filepath, func=ord)
    start_rc = Coordinates(*np.where(array == ord("S")))

    if part == 1:
        array[start_rc] = ord("a") - 1
        start_rcs = [start_rc]
    else:
        array[start_rc] = ord("a")
        start_rcs = [Coordinates(*rc) for rc in zip(*np.where(array == ord("b")))]

    end_rc = Coordinates(*np.where(array == ord("E")))
    array[end_rc] = ord("z") + 1

    steps = np.inf
    for src in start_rcs:
        if steps != (next_min := min(steps, dijkstra(array, src, end_rc))):
            steps = next_min
            print(f"{steps}... ", end="")

    if part == 1:
        print(steps)
    else:
        print(steps + 1)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
