import math
import re

from tools import parse_lines, print_part


def get_numbers(line: str, as_ints: bool = True) -> list[int | str]:
    transformer = int if as_ints else lambda x: x
    return [transformer(num) for num in re.findall(r"\d+", line)]


def parse(line: str, part: int) -> list[int]:
    if part == 1:
        return get_numbers(line)
    else:
        return [int("".join(get_numbers(line, as_ints=False)))]


def get_roots(a: int, b: int, c: int):
    discriminant = b**2 - 4 * a * c
    r1 = (-b + math.sqrt(discriminant)) / (2 * a)
    r2 = (-b - math.sqrt(discriminant)) / (2 * a)
    return min(r1, r2), max(r1, r2)


@print_part
def solve(filepath: str, part: int = 1):
    time, goal = [parse(line, part=part) for line in parse_lines(filepath)]
    num_ways = 1
    for t, g in zip(time, goal):
        roots = get_roots(1, -t, g)
        num_ways *= math.ceil(roots[1] - roots[0])
    print(num_ways)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
