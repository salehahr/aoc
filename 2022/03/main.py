from typing import Callable, Generator, List

import context
from tools import parse_lines, print_part

UNICODE_a_OFFSET = 97
UNICODE_A_OFFSET = 65
NUM_ALPHABET = 26

LOWERCASE_MAP = {chr(i + UNICODE_a_OFFSET): i + 1 for i in range(NUM_ALPHABET)}
UPPERCASE_MAP = {
    chr(i + UNICODE_A_OFFSET - NUM_ALPHABET): i + 1
    for i in range(NUM_ALPHABET, NUM_ALPHABET * 2)
}
PRIORITY_MAP = LOWERCASE_MAP | UPPERCASE_MAP

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


def remove_repeated(str_input: str) -> str:
    """Removes repeated chars in string."""
    return "".join(set(str_input))


def get_duplicate(list_of_strings: Items) -> chr:
    """Gets the first character that is repeated across the list of strings."""
    strings = [remove_repeated(s) for s in list_of_strings]
    for char in strings[0]:
        contained = all([char in string_subgroup for string_subgroup in strings[1:]])
        if contained:
            return char


@print_part
def solve(filepath: str, part: int = 1):
    priorities = 0
    parse_items: callable = split_lines if part == 1 else group_lines(3)

    lines = parse_lines(filepath)
    for list_of_items in parse_items(lines):
        item = get_duplicate(list_of_items)
        priorities += PRIORITY_MAP[item]

    print(priorities)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
