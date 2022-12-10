from typing import Generator

from tools import parse_lines, print_part


def parse_ints(filepath: str) -> Generator[int | None, None, None]:
    """Returns integer value of the current line."""
    lines = parse_lines(filepath)
    for line in lines:
        yield int(line) if line.isdigit() else None


def update_max_calories(cals: int, max_cals_list: list[int], i: int) -> None:
    """
    Updates list containing the top X calories carried.
    The list is sorted in descending order.
    """
    if cals > max_cals_list[i]:
        max_cals_list[i] = cals
    max_cals_list.sort(reverse=True)


def get_next_index(cals: int, max_cals_list: list[int]) -> int:
    """
    If cals is part of max_cals_list, returns the corresponding list index.
    Otherwise returns the last index (smallest value in max_cals_list).
    """
    if cals in max_cals_list:
        return max_cals_list.index(cals)
    else:
        return -1


@print_part
def solve(filepath: str, part: int = 1):
    NUM_BACKUPS = 0 if part == 1 else 2

    current_elf_calories = 0
    max_calories_list = [0] * (NUM_BACKUPS + 1)
    i = -1

    for calorie in parse_ints(filepath):
        current_elf_calories = current_elf_calories + calorie if calorie else 0
        update_max_calories(current_elf_calories, max_calories_list, i)
        i = get_next_index(current_elf_calories, max_calories_list)

    print(sum(max_calories_list))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
