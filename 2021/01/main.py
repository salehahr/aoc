# https://adventofcode.com/2021/day/1
from tools import parse_lines, print_ans, print_part


def window(numbers: list[int], k: int) -> list[int]:
    """
    Slides a window of size k over the list of n numbers and
    sums up the elements in the window.
    Returns a list, with length n - (k - 1), of the window summations.
    """
    sublists = [[]] * k
    for i in range(k):
        j = -k + 1 + i
        sublists[i] = numbers[i : j if j != 0 else None]
    return [sum(nums) for nums in zip(*sublists)]


@print_part
def solve(filepath: str, part: int = 1):
    depths = window([int(n) for n in parse_lines(filepath)], k=1 if part == 1 else 3)
    num_increases = sum(b > a for (a, b) in zip(depths[:-1], depths[1:]))
    print_ans(num_increases)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
