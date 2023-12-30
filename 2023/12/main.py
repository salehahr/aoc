from functools import cache

from tools import parse_lines, print_part

"""
With a lot of help from
https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/
"""


@cache
def handle_hash(record: str, groups: tuple[int, ...]) -> int:
    """
    Go to next substring and consume a group number.
    """
    n = groups[0]

    # no match
    if record[:n].replace("?", "#") != "#" * n:
        return 0
    elif len(record) == n:
        return len(groups) == 1
    elif record[n] in ".?":
        return num_arrangements(record[n + 1 :], groups[1:])

    return 0


@cache
def handle_dot(record, groups) -> int:
    """
    Go to next non-dot value without consuming a group number.
    """
    if next_record := record[1:]:
        return num_arrangements(next_record, groups)
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
