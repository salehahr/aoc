import numpy as np

from tools import parse_lines, print_part


def neighbour_coords(r, c, h, w):
    rcs = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    for ri, ci in rcs:
        if 0 <= ri < h and 0 <= ci < w:
            yield int(ri), int(ci)


def can_climb(src, dst):
    return dst <= (src + 1)


def dijkstra(array, start_rc, end_rc):
    # https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode

    dist_array = np.full(array.shape, np.inf)
    dist_array[start_rc] = 0

    height, width = array.shape
    Q = [(r, c) for r in range(height) for c in range(width)]
    Q.sort(key=lambda x: dist_array[x])

    result = None
    while end_rc in Q:
        rc_u = Q.pop(0)

        neighbour_rcs = [
            v
            for v in neighbour_coords(*rc_u, *array.shape)
            if v in Q and can_climb(array[rc_u], array[v])
        ]

        for v_rc in neighbour_rcs:
            cost = dist_array[rc_u] + 1
            if cost < dist_array[v_rc]:
                dist_array[v_rc] = cost

        Q.sort(key=lambda x: dist_array[x])

    try:
        result = int(dist_array[end_rc])
    except OverflowError:
        result = np.inf
    finally:
        return result


@print_part
def solve(filepath: str, part: int = 1):
    array = np.array([[ord(c) for c in line] for line in parse_lines(filepath)])

    start_rc = np.where(array == ord("S"))
    if part == 1:
        array[start_rc] = ord("a") - 1
        start_rcs = [start_rc]
    else:
        array[start_rc] = ord("a")
        start_rcs = [(x, y) for x, y in zip(*np.where(array == ord("b")))]

    end_rc = np.where(array == ord("E"))
    array[end_rc] = ord("z") + 1

    steps = np.inf
    for src in start_rcs:
        steps = min(steps, dijkstra(array, src, end_rc))
        print(steps)

    if part == 1:
        print(steps)
    else:
        print(steps + 1)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
