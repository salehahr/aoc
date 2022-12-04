# https://adventofcode.com/2021/day/2
import context
import numpy as np

from tools import parse_lines, print_part


def commands_to_tuples(commands_: list[str]) -> list[tuple[int, int]]:
    """
    Given a list of movement commands and their magnitudes,
    parses these into displacement tuples.
    e.g.    forward 5, down 6   becomes ( +5,  +6)
            forward 3, up 20    becomes ( +3, -20)
    """
    command_tuples = [(c.split()[0], int(c.split()[1])) for c in commands_]
    return [
        (0, dist) if mov == "down" else (0, -dist) if mov == "up" else (dist, 0)
        for (mov, dist) in command_tuples
    ]


def calculate_prod_xy(
    xy_displacements: list[tuple[int, int]], with_aim: bool = False
) -> int:
    """
    Returns the product of the total units moved forwards
    with the total units moved downwards.
    If aim calculation is taken into account, the depth calculation is affected,
    thus also affecting the product returned.
    :param xy_displacements: movement commands coded as (+x, +y) displacements
    :param with_aim: whether aim is calculated
    :return: product of total horizontal displacement and total depth
    """
    xv, yv = zip(*xy_displacements)

    if with_aim:
        # The y-part of the tuples is the aim, which is used to calculate the new depth.
        depth = np.array(xv) * np.cumsum(yv)
    else:
        # The y-part of the tuples is the depth.
        depth = yv

    return sum(xv) * sum(depth)


@print_part
def solve(filepath: str, part: int = 1):
    commands = parse_lines(filepath)
    displacements = commands_to_tuples(commands)
    prod_xy = calculate_prod_xy(displacements, with_aim=part == 2)
    print(prod_xy)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
