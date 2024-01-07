import re

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


def parse_input(line: str, part: int) -> [Direction, int]:
    direction, num_steps, hex_code = re.findall(r"(\w) (\d+).*#(\w{6})", line)[0]

    if part == 1:
        direction = DIRECTION_MAP_p1[direction]
        num_steps = int(num_steps)
    else:
        direction = DIRECTION_MAP_p2[int(hex_code[-1])]
        num_steps = int("0x" + hex_code[:-1], 16)

    return direction, num_steps


def traverse(directions: list[Direction], num_steps: list[int], start_rc: Coordinates = Coordinates(0, 0)):
    vertices = [start_rc]

    for direction, steps in zip(directions, num_steps):
        vertices.append(vertices[-1] + (steps * direction.value))

    return vertices


def area_of_polygon(vertices: list[Coordinates]) -> int:
    """
    Uses the shoelace formula to calculate the area of a polygon given its ordered vertices.
    """
    double_area = 0
    ext_vertices = [vertices[-1]] + vertices + [vertices[0]]
    for i in range(1, len(ext_vertices) - 1):
        p_prev, p_curr, p_next = (
            ext_vertices[i - 1],
            ext_vertices[i],
            ext_vertices[i + 1],
        )
        double_area += p_curr.r * (p_prev.c - p_next.c)
    return double_area // 2


@print_part
def solve(filepath: str, part: int):
    directions, num_steps = zip(
        *map(lambda x: parse_input(x, part), parse_lines(filepath))
    )
    vertices = traverse(directions, num_steps)

    perimeter = sum(num_steps)
    area_in = area_of_polygon(vertices)
    total_area = area_in + (perimeter // 2) + 1
    return total_area


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
