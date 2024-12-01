from typing import Iterable

import numpy as np

from tools import parse_lines, print_ans, print_part

Report = tuple[int, ...]


def is_safe(report: Report) -> bool:
    diffs = np.diff(report)
    n_diffs = len(diffs)

    def __all_inc_or_dec() -> bool:
        if 0 in diffs:
            return False
        n_pos_diffs = len([n for n in diffs if n > 0])
        return n_pos_diffs in {0, n_diffs}

    def __min_one_max_three() -> bool:
        n_in_range = len([d for d in diffs if 1 <= abs(d) <= 3])
        return n_in_range == n_diffs

    return __all_inc_or_dec() and __min_one_max_three()


def alternative_reps(report: Report) -> Iterable[Report]:
    for i in range(len(report)):
        if i == 0:
            yield report[1:]
        elif i == (len(report) - 1):
            yield report[:-1]
        else:
            yield *report[:i], *report[i + 1 :]


@print_part
def solve(filepath: str, part: int = 1):
    reports = [tuple(map(int, line.split())) for line in parse_lines(filepath)]
    safe_reps = list(filter(is_safe, reports))
    n_safe_reps = len(safe_reps)

    if part == 1:
        print_ans(n_safe_reps, correct_ans=624)
    elif part == 2:
        for unsafe_rep in set(reports) - set(safe_reps):
            new_reports = alternative_reps(report=unsafe_rep)
            n_safe_reps += any(map(is_safe, new_reports))
        print_ans(n_safe_reps, correct_ans=658)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
