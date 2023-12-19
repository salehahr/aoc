import re
import time

import numpy as np


def parse_lines(filepath: str, strip: bool = True) -> list[str]:
    """
    Returns a list of the lines contained within the file.
    """
    with open(filepath, "r") as file:
        lines = file.readlines()
    return [line.strip() if strip else line for line in lines]


def get_array(filepath: str, func: callable = None) -> np.array:
    apply_func = generate_callback(func)
    return np.array([[apply_func(c) for c in line] for line in parse_lines(filepath)])


def generate_callback(func: callable = None) -> callable:
    if func:

        def __wrapped_function(arg):
            return func(arg)

    else:

        def __wrapped_function(arg):
            return arg

    return __wrapped_function


def peek(filepath: str, n: int = 1) -> str | list[str]:
    """
    Returns the first n lines of the file.
    """
    with open(filepath, "r") as file:
        if n == 1:
            return file.readline().strip()
        else:
            return [file.readline().strip() for _ in range(n)]


def print_part(func):
    """
    Prints header for current part being solved.
    """

    def _wrapped(*args, **kwargs):
        part = kwargs["part"]
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start

        if result:
            print(f"Part {part} ({duration:.4f} s)")
            print(f"{result}\n")
        else:
            print(f"Part {part} ({duration:.4f} s)\n")

    return _wrapped


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def get_numbers(
    line: str, include_sign: bool = False, as_ints: bool = True
) -> list[int | str]:
    num_pattern = r"\d+"
    if include_sign:
        num_pattern = r"[+-]?" + num_pattern
    return [
        int(num_str) if as_ints else num_str
        for num_str in re.findall(num_pattern, line)
    ]


def flatten_list(list_: list) -> list:
    return [vv for v in list_ for vv in v]


def print_ans(ans, correct_ans=None):
    if correct_ans:
        error_message = f"\nExpected {correct_ans},"
        error_message += f"\ngot      {ans}"
        assert ans == correct_ans, error_message
    print(ans)


def ienumerate(*args):
    return enumerate(zip(*args))
