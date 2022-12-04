import re
from typing import Generator

import context
from tools import parse_lines, print_part

PairSections = tuple[int, int, int, int]


def parse_sections(filepath: str) -> Generator[PairSections, None, None]:
    """Returns the current pair sections."""
    for line in parse_lines(filepath):
        yield [int(num) for num in re.findall(r"(\d+)", line)]


def overlap(start1: int, end1: int, start2: int, end2: int) -> bool:
    """
    Checks whether sections overlap.
            s1 --- e1
    --- e2             s2 ---
    """
    if end2 < start1 or end1 < start2:
        return False
    else:
        return True


def fully_contained(start1: int, end1: int, start2: int, end2: int) -> bool:
    """Checks whether a section is fully contained in the other."""
    if (start2 >= start1 and end2 <= end1) or (start1 >= start2 and end1 <= end2):
        return True
    else:
        return False


@print_part
def solve(filepath: str, part: int = 1):
    checker: callable = fully_contained if part == 1 else overlap
    duplicates = 0

    for sections in parse_sections(filepath):
        duplicates += checker(*sections)

    print(duplicates)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
