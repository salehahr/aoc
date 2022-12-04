from typing import Callable, Generator, List

import context
from tools import parse_lines, print_part

NUM_ALPHABET = 26

Items = list[str]
ItemsGenerator = Generator[Items, None, None]


def split_lines(lines: Items) -> ItemsGenerator:
    """Yields two equal halves of the current line."""
    for line in lines:
        n = len(line) // 2
        yield line[:n], line[n:]


def group_lines(partition_size: int) -> Callable[[Items], ItemsGenerator]:
    """Yields lines in groups of partition_size."""

    def _grouper(lines: Items) -> ItemsGenerator:
        for i in range(0, len(lines), partition_size):
            yield lines[i : i + partition_size]

    return _grouper


def get_duplicate(strings: Items) -> chr:
    """Gets the first character that is repeated across the list of strings."""
    for char in strings[0]:
        contained = all([char in string_subgroup for string_subgroup in strings[1:]])
        if contained:
            return char


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    parse_items: callable = split_lines if part == 1 else group_lines(3)

    priorities = 0
    for items in parse_items(lines):
        item = get_duplicate(items)

        if item.islower():
            priorities += ord(item) - ord("a") + 1
        else:
            priorities += ord(item) - ord("A") + 1 + NUM_ALPHABET

    print(priorities)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
