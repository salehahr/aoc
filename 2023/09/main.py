import numpy as np
from tools import get_numbers, parse_lines, print_part


def get_edge_values(line0: list[int], part: int):
    """
    Returns the edge value for each level, going across each diff level until diff == 0 is reached.
    """
    index = -1 if part == 1 else 0
    edge_vals, diffs = [line0[index]], line0
    while np.any(diffs):
        diffs = np.diff(diffs)
        edge_vals.append(diffs[index])
    return edge_vals


def extrapolator(line0: list[int], part: int):
    """
    Extrapolates the next value in the sequence.
    """
    edge_values = get_edge_values(line0, part)
    if part == 1:
        return sum(edge_values)
    else:
        return sum(edge_values[::2]) - sum(edge_values[1::2])  # a - b + c - d + e ...


@print_part
def solve(filepath: str, part: int):
    lines = [get_numbers(line, include_sign=True) for line in parse_lines(filepath)]
    result = sum([extrapolator(line, part) for line in lines])
    print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
