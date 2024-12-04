from functools import cache

from tools import get_numbers, parse_lines, print_ans, print_part


@cache
def blink(stone: int, n: int) -> int:
    if n == 0:
        return 1
    elif stone == 0:
        return blink(1, n - 1)
    elif len(stone_str := str(stone)) % 2 == 0:
        split_idx = len(stone_str) // 2
        s1, s2 = map(int, (stone_str[:split_idx], stone_str[split_idx:]))
        return blink(s1, n - 1) + blink(s2, n - 1)
    else:
        return blink(stone * 2024, n - 1)


@print_part
def solve(filepath: str, part: int = 1):
    stones = get_numbers(parse_lines(filepath)[0])
    ans = sum(blink(stone, 25 if part == 1 else 75) for stone in stones)
    print_ans(ans, correct_ans=175006 if part == 1 else 207961583799296)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
