import math
import re

from tools import parse_lines, print_part

SYMBOL_PATTERN = r"[^.\d\s]"
GEAR_PATTERN = r"\*"
NUMBER_PATTERN = r"\d+"


def tb_indices(current_line_index: int, max_num_lines: int) -> range:
    top, bottom = max(0, current_line_index - 1), min(
        current_line_index + 2, max_num_lines
    )
    return range(top, bottom)


def get_surrounding_lines(top_bottom: range, lines: list[str]) -> list[str]:
    return [lines[y] for y in range(top_bottom.start, min(top_bottom.stop, len(lines)))]


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    line_length, num_lines = len(lines[0]), len(lines)

    symbol_pattern = SYMBOL_PATTERN if part == 1 else GEAR_PATTERN
    result = 0

    for row, current_line in enumerate(lines):
        top_bottom_indices = tb_indices(row, max_num_lines=num_lines)

        for symbol_match in re.finditer(symbol_pattern, current_line):
            mid_indices = set(range(symbol_match.start(0) - 1, symbol_match.end(0) + 1))

            neighbouring_numbers = []
            for surr_line in get_surrounding_lines(top_bottom_indices, lines):
                for number_match in re.finditer(NUMBER_PATTERN, surr_line):
                    number_span = set(range(*number_match.span()))
                    if number_span & mid_indices:
                        neighbouring_numbers.append(int(number_match[0]))

            if part == 1:
                result += sum(neighbouring_numbers)
            elif len(neighbouring_numbers) == 2:
                result += math.prod(neighbouring_numbers)

    print(result)


if __name__ == "__main__":
    FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
