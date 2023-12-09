import re


def parse_lines(filepath: str, strip: bool = True) -> list[str]:
    """
    Returns a list of the lines contained within the file.
    """
    with open(filepath, "r") as file:
        lines = file.readlines()
    return [line.strip() if strip else line for line in lines]


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
        print(f"\nPart {kwargs['part']}")
        return func(*args, **kwargs)

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


def print_ans(ans, correct_ans=None):
    if correct_ans:
        assert ans == correct_ans
    print(ans)
