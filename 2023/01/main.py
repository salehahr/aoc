import itertools
import re

from tools import parse_lines, print_part

DIGITS_AS_TEXT = (
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def get_digit(text_: str, part: int, reverse: bool) -> str:
    """
    Extracts the digit from a string.
    """
    if text_.isdigit():
        return text_
    elif part == 2:
        text = reversed(text_) if reverse else text_
        for substring in itertools.accumulate(text):
            substring = "".join(reversed(substring)) if reverse else substring
            for DIGIT in DIGITS_AS_TEXT:
                if DIGIT in substring:
                    return str(DIGITS_AS_TEXT.index(DIGIT) + 1)


def get_first_last_digit(line_: str, parser: callable) -> int:
    """
    Returns the number consisting of the first and last digit of the line.
    """

    partitions = [p for p in re.split(r"(\d)", line_) if p]
    first, last = None, None

    for partition_fwd, partition_bwd in zip(partitions, reversed(partitions)):
        if not first:
            first = parser(partition_fwd, reverse=False)
        if not last:
            last = parser(partition_bwd, reverse=True)
        if first and last:
            break

    if first is None and last is None:
        return 0

    return int(first + last)


def get_first_last_digits(filepath: str, part: int):
    """
    For each line in the file, returns the number consisting of the first and last digit of the line.
    """

    def __digit_parser(text: str, reverse: bool):
        return get_digit(text, part, reverse)

    for line in parse_lines(filepath):
        yield get_first_last_digit(line, parser=__digit_parser)


@print_part
def solve(filepath: str, part: int = 1):
    result = sum(get_first_last_digits(filepath, part=part))
    print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
