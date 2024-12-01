from tools import parse_lines, print_ans, print_part


@print_part
def solve(filepath: str, part: int = 1):
    left, right = zip(*((map(int, line.split()) for line in parse_lines(filepath))))

    if part == 1:
        ans = sum(abs(nl - nr) for nl, nr in zip(sorted(left), sorted(right)))
        print_ans(ans, correct_ans=2000468)
    elif part == 2:
        ans = sum(nl * right.count(nl) for nl in left)
        print_ans(ans, correct_ans=18567089)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
