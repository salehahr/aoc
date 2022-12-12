from tools import parse_lines, print_part

SNAFU_REM_DICT = {0: "0", 1: "1", 2: "2", 3: "=", 4: "-"}
SNAFU_SYM_DICT = {"0": 0, "1": 1, "2": 2, "=": -2, "-": -1}
BASE = 5
LOWER_BOUNDARY = 3


def dec2snafu(dec: int) -> str:
    s = ""
    while dec:
        remainder = dec % BASE
        s = SNAFU_REM_DICT[remainder] + s

        if remainder >= LOWER_BOUNDARY:
            dec += BASE - remainder

        dec //= BASE

    return s


def snafu2dec(snafu: str) -> int:
    return sum([BASE**i * SNAFU_SYM_DICT[s] for i, s in enumerate(reversed(snafu))])


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)

    if part == 1:
        dec_sum = sum([snafu2dec(s) for s in lines])
        print(dec2snafu(dec_sum))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
