import re

from tools import parse_lines, print_ans, print_part


def is_bad_p1(line: str) -> bool:
    contains_bad_ss = any([bad_ss in line for bad_ss in ["ab", "cd", "pq", "xy"]])
    no_repeated = re.search(r"(.)\1{1,}", line) is None
    less_3_vowels = re.search(r"[aeiou].*[aeiou].*[aeiou]", line) is None
    return contains_bad_ss or no_repeated or less_3_vowels


def is_nice_p2(line: str) -> bool:
    is_pair_match = re.match(r".*(..)(.*)\1.*", line) is not None
    is_aba_match = re.search(r".*(.)(.)\1.*", line) is not None
    return is_pair_match and is_aba_match


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    if part == 1:
        print_ans(sum([1 for line in lines if not is_bad_p1(line)]), 238)
    else:
        print_ans(sum([int(is_nice_p2(line)) for line in lines]), 69)


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
