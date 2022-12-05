from tools import parse_lines, print_part


@print_part
def solve(filepath: str, part: int = 1):
    num_distinct = 4 if part == 1 else 14

    for i, c in enumerate(parse_lines(filepath)[0]):
        packet = line[i : i + num_distinct]
        if len(set(packet)) == num_distinct:
            print(i + num_distinct, packet)
            break


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
