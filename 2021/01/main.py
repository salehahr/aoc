# https://adventofcode.com/2021/day/1
import context

from tools import parse_lines, print_part


def window(numbers: list[int], k: int) -> list[int]:
    """
    Slides a window of size k over the list of n numbers and
    sums up the elements in the window.
    Returns a list, with length n - (k - 1), of the window summations.
    """
    sublists = [[]] * k

    for i in range(k):
        j = -k + 1 + i
        if j != 0:
            sublists[i] = numbers[i : -k + 1 + i]
        else:
            sublists[i] = numbers[i:]

    return [sum(nums) for nums in zip(*sublists)]


def get_number_of_increases(numbers: list[int]) -> int:
    """
    Given a list of numbers, returns the number
    of elements that are greater than the previous.
    """
    return sum(b > a for (a, b) in zip(numbers[:-1], numbers[1:]))


@print_part
def solve(filepath: str, part: int = 1):
    depths = [int(line) for line in parse_lines(filepath)]

    if part == 2:
        depths = window(depths, k=3)

    num_increases = get_number_of_increases(depths)
    print(num_increases)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
