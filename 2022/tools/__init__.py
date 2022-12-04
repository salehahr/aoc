def parse_lines(filepath: str) -> list[str]:
    with open(filepath) as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def print_part(func):
    def _wrapped(*args, **kwargs):
        print(f"\nPart {kwargs['part']}")
        return func(*args, **kwargs)

    return _wrapped
