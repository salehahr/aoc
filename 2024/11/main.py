from functools import cache

from tools import flatten, get_numbers, parse_lines, print_ans, print_part


@cache
def blink(stone: int) -> int | tuple[int, ...]:
    if stone == 0:
        return 1
    elif len(stone_str := str(stone)) % 2 == 0:
        split_idx = len(stone_str) // 2
        return tuple(map(int, (stone_str[:split_idx], stone_str[split_idx:])))
    else:
        return stone * 2024


@print_part
def solve(filepath: str, part: int = 1):
    stones = get_numbers(parse_lines(filepath)[0])
    for b in range(25 if part == 1 else 75):
        stones = flatten(map(blink, stones))
    ans = len(list(stones))
    print_ans(ans, correct_ans=175006 if part == 1 else None)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    # solve(FILEPATH, part=2)
