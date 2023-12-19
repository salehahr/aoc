import re
from collections import defaultdict

from tools import parse_lines, print_part
from tools.generic_types import Coordinates, Direction

DIRECTION_MAP_p1 = {
    "R": Direction.RIGHT,
    "L": Direction.LEFT,
    "U": Direction.UP,
    "D": Direction.DOWN,
}
DIRECTION_MAP_p2 = {
    0: Direction.RIGHT,
    1: Direction.DOWN,
    2: Direction.LEFT,
    3: Direction.UP,
}


def count_tiles(
    vertical_coords: list[Direction, Coordinates],
    horizontal_edges: dict[int, list[range]],
) -> [int, int]:
    tiles_between_ud, tiles_between_du = 0, 0
    rows: dict[int, list[[Direction, int]]] = defaultdict(list)

    for direction, (row, col) in vertical_coords:
        rows[row].append((direction, col))

    for row, dir_cols in rows.items():
        dir_cols.sort(key=lambda dir_col: dir_col[-1])

        for i in range(len(dir_cols) - 1):
            dir0, start0 = dir_cols[i]
            dir1, start1 = dir_cols[i + 1]

            if dir0 == dir1:
                continue

            cols = range(start0 + 1, start1)
            len_cols = start1 - (start0 + 1)

            if dir0 == Direction.UP and dir1 == Direction.DOWN:
                if cols not in horizontal_edges.get(row, []):
                    tiles_between_ud += len_cols
            elif dir0 == Direction.DOWN and dir1 == Direction.UP:
                if cols not in horizontal_edges.get(row, []):
                    tiles_between_du += len_cols

    return tiles_between_ud, tiles_between_du


def parse_input(line: str, part: int) -> [Direction, int]:
    direction, num_steps, hex_code = re.findall(r"(\w) (\d+).*#(\w{6})", line)[0]

    if part == 1:
        direction = DIRECTION_MAP_p1[direction]
        num_steps = int(num_steps)
    else:
        direction = DIRECTION_MAP_p2[int(hex_code[-1])]
        num_steps = int("0x" + hex_code[:-1], 16)

    return direction, num_steps


def traverse(directions: list[Direction], num_steps: list[int], start_rc: Coordinates):
    loop = [start_rc]
    vertical_coords = [(directions[0], start_rc)]
    horizontal_edges = defaultdict(list)
    vertices = []

    for direction, steps in zip(directions, num_steps):
        prev_vdir = vertical_coords[-1][0]

        loop_seg = [loop[-1] + i * direction.value for i in range(1, steps + 1)]
        loop += loop_seg
        vertices.append(loop_seg[-1])

        match direction:
            case Direction.UP | Direction.DOWN:
                if prev_vdir != direction:  # turn
                    vertical_coords[-1] = (direction, vertical_coords[-1][-1])
                vertical_coords += [(direction, lrc) for lrc in loop_seg[-steps:]]
            case Direction.LEFT | Direction.RIGHT:
                vertical_coords += [(prev_vdir, loop[-1])]
                cols = [loop_seg[i].c for i in [0, -1]]
                if cols[0] > cols[1]:
                    loop_seg_c = range(cols[1] + 1, cols[0] + 1)
                else:
                    loop_seg_c = range(*cols)
                if loop_seg_c:
                    horizontal_edges[loop_seg[0].r].append(loop_seg_c)

    vertical_coords[0] = vertical_coords.pop(-1)

    return loop, vertical_coords, horizontal_edges, vertices


def shoelace(vertices: list[Coordinates]) -> int:
    double_A = 0
    if not isinstance(vertices[0], Coordinates):
        vertices = [Coordinates(*v) for v in vertices]
    # vertices = [Coordinates(0 if v.r == 0 else v.r + 1, 0 if v.c == 0 else v.c + 1) for v in vertices]
    print(vertices)
    ext_vertices = [vertices[-1]] + vertices + [vertices[0]]
    for i in range(1, len(ext_vertices) - 1):
        p_prev, p_curr, p_next = (
            ext_vertices[i - 1],
            ext_vertices[i],
            ext_vertices[i + 1],
        )
        double_A += p_curr.r * (p_prev.c - p_next.c)
    return double_A // 2


@print_part
def solve(filepath: str, part: int):
    directions, num_steps = zip(
        *map(lambda x: parse_input(x, part), parse_lines(filepath))
    )
    start_rc = Coordinates(0, 0)

    loop, vertical_coords, horizontal_edges, vertices = traverse(
        directions, num_steps, start_rc
    )
    # sum_ = shoelace(vertices)
    # s1 = shoelace([(0,0), (0,6+1)R, (5+1, 6+1)RD, (5+1, 2-1)DL, (2+1, 2-1)LU, (2+1, 0)U])
    # s1 = shoelace(
    #     [(0, 0), (0, 6 + 1), (5 + 1, 6 + 1), (5 + 1, 2), (2 + 1, 2), (2 + 1, 0)]
    # )
    # print(vertices, sum_, s1)
    # assert False

    num_loop = len(set(loop))
    g1, g2 = count_tiles(vertical_coords, horizontal_edges)

    return f"{num_loop=} | {num_loop+g1=} | {num_loop+g2=}"


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    # FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
