from typing import Generator, Union


def str2int(line: str) -> Union[int, None]:
    return int(line) if line.isdigit() else None


def parse_lines(filepath: str) -> list[str]:
    with open(filepath) as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def parse_all_ints(filepath: str) -> list[Union[int, None]]:
    lines = parse_lines(filepath)
    return [str2int(line) for line in lines]


def parse_ints(filepath: str) -> Generator[Union[int, None], None, None]:
    lines = parse_lines(filepath)
    for line in lines:
        yield str2int(line)
