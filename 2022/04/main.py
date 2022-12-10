import re
from typing import Generator

from tools import parse_lines, print_part

PairSections = tuple[int, int, int, int]


def parse_sections(filepath: str) -> Generator[PairSections, None, None]:
    """Returns the current pair sections."""
    for line in parse_lines(filepath):
        elf_pair = [int(num) for num in re.findall(r"(\d+)", line)]
        yield reorder_elf_pair(*elf_pair)


def reorder_elf_pair(start1: int, end1: int, start2: int, end2: int) -> PairSections:
    """Reorders the pair so that the smallest start value is the first item."""
    return (
        (start2, end2, start1, end1)
        if start1 > start2
        else (start1, end1, start2, end2)
    )


def overlap(start1: int, end1: int, start2: int, end2: int) -> bool:
    """Checks whether sections overlap."""
    # --- same starts: always overlapping
    if start1 == start2 or end1 == end2:
        return True

    # --- different starts: possibly overlapping
    if end1 < start2:
        return False
    else:
        return True


def fully_contained(start1: int, end1: int, start2: int, end2: int) -> bool:
    """Checks whether a section is fully contained in the other."""
    # --- no overlaps: no containment
    if not overlap(start1, end1, start2, end2):
        return False

    # --- overlapping with same starts: always fully-contained
    if start1 == start2 or end1 == end2:
        return True

    # --- overlapping with different starts: possibly fully-contained
    # fully contained if section is a single number
    if end1 == start2:
        return True if start1 == end1 or start2 == end2 else False
    # fully contained if end2 < end1
    else:
        return False if end2 > end1 else True


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
