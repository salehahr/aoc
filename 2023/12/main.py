import re
from functools import cache

from tools import parse_lines, print_part

"""
With a lot of help from
https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/
"""


ignore_hash_before = r"(?<!#)"
ignore_hash_after = r"(?!#)"


def base_pattern(num: int):
    num_str = "{" + str(num) + "}"
    return rf"{ignore_hash_before}[?#]{num_str}{ignore_hash_after}"


@cache
def handle_hash(record: str, groups: tuple[int, ...]) -> int:
    """
    Go to next substring and consume a group number.
    """
    n = groups[0]

    # no overall match for groups
    if re.match(".+?".join([base_pattern(x) for x in groups]), record) is None:
        return 0
    # final match
    elif record == re.match(base_pattern(n), record)[0]:
        return 1

    return num_arrangements(record[n + 1 :], groups[1:])


@cache
def handle_dot(record, groups) -> int:
    """
    Go to next non-dot value without consuming a group number.
    """
    if next_non_dot := re.search(r"[^.]", record[1:]):
        s = next_non_dot.start() + 1
        return num_arrangements(record[s:], groups)
    return 0


@cache
def num_arrangements(record: str, groups):
    if not groups:
        return "#" not in record
    elif not record:
        return 0
    else:
        match record[0]:
            case "#":
                return handle_hash(record, groups)
            case ".":
                return handle_dot(record, groups)
            case "?":
                return handle_hash(record, groups) + handle_dot(record, groups)


@print_part
def solve(filepath: str, part: int):
    records, record_groups = zip(*map(lambda x: x.split(" "), parse_lines(filepath)))
    record_groups = [tuple(map(int, n.split(","))) for n in record_groups]

    if part == 2:
        records = map(lambda x: "?".join([x] * 5), records)
        record_groups = tuple(map(lambda x: tuple(list(x) * 5), record_groups))

    result = 0
    for record, groups in zip(records, record_groups):
        result += num_arrangements(record, groups)
    print(f"{result=}")


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
