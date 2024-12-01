import math
import re

from tools import parse_lines, print_ans, print_part


def get_product(line: str) -> int:
    mult_pattern = r"\(\d+,\d+\)"

    def __mult_numbers(line_: str) -> tuple[int, int] | None:
        if match := re.match(mult_pattern, line_):
            return eval(match.group(0))

    num_pairs = map(__mult_numbers, line.split("mul"))
    return sum(math.prod(np) for np in num_pairs if np)


@print_part
def solve(filepath: str, part: int = 1):
    lines = "".join(parse_lines(filepath))
    prods = get_product(lines)

    if part == 1:
        print_ans(prods, correct_ans=178886550)
    else:
        _, *donts = lines.split("don't()")
        for dont in donts:
            nok, *_ = dont.split("do()")
            prods -= get_product(nok)
        print_ans(prods, correct_ans=87163705)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
