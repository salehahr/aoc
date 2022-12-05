def parse_lines(filepath: str, strip:bool = True) -> list[str]:
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
