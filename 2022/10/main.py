from tools import parse_lines, print_part

INTERVAL = 40


def draw_line(line: str, cycle: int, x: int) -> str:
    line += "█" if pixel(cycle) in sprite_coordinates(x) else "-"

    if len(line) % INTERVAL == 0:
        print(line)
        line = ""

    return line


def pixel(current_cycle: int) -> int:
    return (current_cycle - 1) % 40


def sprite_coordinates(x: int) -> list[int]:
    return [x - 1, x, x + 1]


@print_part
def solve(filepath: str, part: int = 1):
    commands = (
        None if len(line.split()) == 1 else int(line.split()[1])
        for line in parse_lines(filepath)
    )

    current_cycle = 1
    register = 1

    p1_signal_strength = 0
    p2_line = ""

    for value in commands:
        num_cycles = 1 if value is None else 2

        for do_update_register in [False, True][:num_cycles]:
            if part == 1:
                p1_signal_strength += (
                    current_cycle * register if current_cycle % INTERVAL == 20 else 0
                )
            else:
                p2_line = draw_line(p2_line, current_cycle, register)

            if do_update_register:
                register += value

            current_cycle += 1

    if part == 1:
        print(p1_signal_strength)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
