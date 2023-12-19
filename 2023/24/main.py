import re
from itertools import combinations
from typing import NamedTuple, Optional

from tools import parse_lines, print_part

NUM_PATTERN = r"[-]?\d+"
COORDS_PATTERN = rf"({NUM_PATTERN}.+{NUM_PATTERN}.+{NUM_PATTERN})"


class Coordinates2D(NamedTuple):
    x: float
    y: float

    def __repr__(self) -> str:
        return repr(tuple(self))


class Equation2D(NamedTuple):
    p0: Coordinates2D
    v0: Coordinates2D

    @property
    def m(self):
        return self.v0.y / self.v0.x

    @property
    def c(self):
        return self.p0.y - self.m * self.p0.x


def gaussian_elimination_2d(
    eq1: Equation2D, eq2: Equation2D
) -> Optional[Coordinates2D]:
    """
            y - mx = c

      E1:   y - m1x = c1
    - E2:   y - m2x = c2
    -------------------------
          (-m1+m2)x = (c1-c2)
    """
    if eq1.m == eq2.m:
        return None

    x = (eq1.c - eq2.c) / (eq2.m - eq1.m)
    y = eq1.m * x + eq1.c

    return Coordinates2D(x, y)


def point_in_future(point: Coordinates2D, eqn1: Equation2D, eqn2: Equation2D) -> bool:
    is_future1 = (point.x > eqn1.p0.x) if (eqn1.v0.x > 0) else (point.x < eqn1.p0.x)
    is_future2 = (point.x > eqn2.p0.x) if (eqn2.v0.x > 0) else (point.x < eqn2.p0.x)
    return is_future1 and is_future2


def point_in_test_range(point: Coordinates2D, min_val: int, max_val: int) -> bool:
    in_range_x = min_val <= point.x <= max_val
    in_range_y = min_val <= point.y <= max_val
    return in_range_x and in_range_y


@print_part
def solve(filepath: str, part: int):
    lines = [
        re.search(rf"{COORDS_PATTERN} @ *{COORDS_PATTERN}", line).groups()
        for line in parse_lines(filepath)
    ]
    equations = [None] * len(lines)
    for i, (p0_str, v0_str) in enumerate(lines):
        p0, v0 = map(
            lambda x: Coordinates2D(*[int(xx) for xx in x.split(", ")[:2]]),
            (p0_str, v0_str),
        )
        equations[i] = Equation2D(p0, v0)

    ct = 0
    for eq1, eq2 in combinations(equations, 2):
        if (intersection := gaussian_elimination_2d(eq1, eq2)) is None:
            continue

        min_val, max_val = (
            (7, 27) if "short" in filepath else (200000000000000, 400000000000000)
        )
        if not point_in_test_range(intersection, min_val, max_val):
            continue
        elif not point_in_future(intersection, eq1, eq2):
            continue
        else:
            ct += 1

    print(ct)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
