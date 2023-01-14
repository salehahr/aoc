import re
from dataclasses import dataclass
from typing import Optional

from tools import parse_lines, print_ans, print_part

PATTERN = r"(\d+)x(\d+)x(\d+)"


@dataclass
class Box:
    l: int
    w: int
    h: int

    @property
    def paper(self) -> int:
        sides = sorted([self.l * self.w, self.w * self.h, self.h * self.l])
        return 2 * sum(sides) + sides[0]

    @property
    def ribbon(self):
        dims = sorted([self.l, self.w, self.h])
        return 2 * sum(dims[:2]) + (self.l * self.w * self.h)


@print_part
def solve(filepath: str, part: int = 1):
    dims = [
        map(int, re.match(PATTERN, line).groups()) for line in parse_lines(filepath)
    ]
    ans = sum([getattr(Box(*d), "paper" if part == 1 else "ribbon") for d in dims])
    print_ans(ans)


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
