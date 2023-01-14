from tools import parse_lines, print_ans, print_part


@print_part
def solve(filepath: str, part: int = 1):
    line = list(parse_lines(filepath)[0])

    if part == 1:
        num_up = sum([1 for c in line if c == "("])
        print_ans(num_up * 2 - len(line))
    else:
        ctr = 0
        for i, c in enumerate(line, start=1):
            ctr = (ctr + 1) if c == "(" else (ctr - 1)
            if ctr == -1:
                print_ans(i)
                break


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
