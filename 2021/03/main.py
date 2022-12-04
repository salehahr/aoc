# https://adventofcode.com/2021/day/3
import enum

import context
import numpy as np

from tools import parse_lines, print_part


def binary_to_decimal(binary_number: np.ndarray) -> int:
    """
    Converts binary representation to decimal integer.
    """
    return int("".join([str(int(b)) for b in binary_number]), 2)


def calculate_gamma_rate(number_ones_across: np.ndarray, total_numbers: int) -> int:
    """
    Calculates gamma rate based on the number of ones
    across the diagnostics array.
    The bits of the gamma rate correspond to the most common
    bit across the diagnostics array.
    """
    binary_rate = number_ones_across > (total_numbers / 2)
    return binary_to_decimal(binary_rate)


def calculate_epsilon_rate(number_ones_across: np.ndarray, total_numbers: int) -> int:
    """
    Calculates epsilon rate based on the number of ones
    across the diagnostics array.
    The bits of the epsilon rate correspond to the least common
    bit across the diagnostics array.
    """
    binary_rate = number_ones_across < (total_numbers / 2)
    return binary_to_decimal(binary_rate)


def calculate_power(diagnostics_: np.ndarray) -> int:
    """
    Returns power consumption as the product of the gamma and epsilon rate.
    """
    total_numbers, _ = diagnostics_.shape
    number_ones_across = np.sum(diagnostics_, 0)

    gamma_rate = calculate_gamma_rate(number_ones_across, total_numbers)
    epsilon_rate = calculate_epsilon_rate(number_ones_across, total_numbers)

    return gamma_rate * epsilon_rate


class BitCriteria(enum.Enum):
    LEAST_COMMON = 0
    MOST_COMMON = 1


def get_gas_rating(diagnostics_: np.ndarray, bit_criteria: BitCriteria) -> int:
    _, bitlength = diagnostics_.shape
    diag = np.copy(diagnostics_)

    for i in range(bitlength):
        num_ones = sum(diag.T[i])
        total_numbers, _ = diag.shape

        if num_ones > (total_numbers / 2):
            diag = diag[diag[:, i] == bit_criteria.value]
        elif num_ones < (total_numbers / 2):
            diag = diag[diag[:, i] != bit_criteria.value]
        else:
            diag = diag[diag[:, i] == bit_criteria.value]

        if diag.shape[0] == 1:
            break

    return binary_to_decimal(diag[0])


def calculate_life_support_rating(diagnostics_: np.ndarray) -> int:
    """
    Returns life support rating as the product of O2 and CO2 ratings.
    """
    o2_rating = get_gas_rating(diagnostics_, BitCriteria.MOST_COMMON)
    co2_rating = get_gas_rating(diagnostics_, BitCriteria.LEAST_COMMON)

    return o2_rating * co2_rating


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    diagnostics = np.array([[int(x) for x in line] for line in lines])

    if part == 1:
        result = calculate_power(diagnostics)
    else:
        result = calculate_life_support_rating(diagnostics)
    print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
