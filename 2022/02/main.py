from enum import Enum

import context
from tools import parse_lines, print_part


class Result(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class Choice(Enum):
    ROCK = 1
    PAPER = 2
    SCISSCORS = 3


class PlayerChoice(Enum):
    A = Choice.ROCK.value
    B = Choice.PAPER.value
    C = Choice.SCISSCORS.value

    X = Choice.ROCK.value
    Y = Choice.PAPER.value
    Z = Choice.SCISSCORS.value


class Outcome(Enum):
    X = [Result.DRAW.value, Result.LOSE.value, Result.WIN.value]
    Y = [Result.WIN.value, Result.DRAW.value, Result.LOSE.value]
    Z = [Result.LOSE.value, Result.WIN.value, Result.DRAW.value]


class DesiredOutcome(Enum):
    X = Result.LOSE.value
    Y = Result.DRAW.value
    Z = Result.WIN.value


class DesiredChoice(Enum):
    X = [Choice.SCISSCORS.value, Choice.ROCK.value, Choice.PAPER.value]
    Y = [Choice.ROCK.value, Choice.PAPER.value, Choice.SCISSCORS.value]
    Z = [Choice.PAPER.value, Choice.SCISSCORS.value, Choice.ROCK.value]


def parse(filepath: str) -> tuple[chr, chr]:
    """Yields first and second column of the current line."""
    lines = parse_lines(filepath)
    for line in lines:
        yield line.split()


@print_part
def solve(filepath: str, part: int = 1):
    result = 0

    for col1, col2 in parse(filepath):
        opponent_choice_index: int = PlayerChoice[col1].value - 1

        if part == 1:
            my_choice: int = PlayerChoice[col2].value
            outcome: int = Outcome[col2].value[opponent_choice_index]
        else:
            my_choice: int = DesiredChoice[col2].value[opponent_choice_index]
            outcome: int = DesiredOutcome[col2].value

        result += outcome + my_choice

    print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
