from tools import parse_lines, print_ans, print_part


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    if part == 1:
        print_ans(sum([len(line) - len(eval(line)) for line in lines]), 1342)
    if part == 2:
        new_lines = [
            line.replace(r"\ "[:-1], "@@")
            .replace(r'"', r"PP", line.count(r'"') - 2)
            .replace(r'"', "xxx")
            for line in lines
        ]
        print_ans(sum([len(nl) - len(l) for nl, l in zip(new_lines, lines)]), 2074)


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
