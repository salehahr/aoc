from tools import parse_lines, print_part


def is_repeated(char: chr, string: str):
    return bool(string.count(char) - 1)


@print_part
def solve(filepath: str, part: int = 1):
    num_distinct = 4 if part == 1 else 14

    for line in parse_lines(filepath):
        for i, c in enumerate(line[:-num_distinct]):
            packet = line[i:i+num_distinct]
            not_repeated = [not is_repeated(c, packet) for c in packet]

            if all(not_repeated):
                print(i+num_distinct, packet)
                break


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
