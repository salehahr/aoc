import math
import re

from tools import get_numbers, parse_lines, print_part


def parse(line: str, part: int) -> list[int]:
    if part == 1:
        return get_numbers(line)
    else:
        return [int("".join(get_numbers(line, as_ints=False)))]


def get_roots(a: int, b: int, c: int):
    discriminant = b**2 - 4 * a * c
    r1 = (-b - math.sqrt(discriminant)) / (2 * a)
    r2 = (-b + math.sqrt(discriminant)) / (2 * a)
    roots_are_int = all([int(r) == r for r in [r1, r2]])
    return r1, r2, roots_are_int


@print_part
def solve(filepath: str, part: int = 1):
    time, goal = [parse(line, part=part) for line in parse_lines(filepath)]
    num_ways = 1
    for t, g in zip(time, goal):
        *roots, are_int = get_roots(1, -t, g)
        num_ways *= math.floor(roots[1]) - math.floor(roots[0]) - are_int
    print(num_ways)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
