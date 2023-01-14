import re

from tools import parse_lines, print_ans, print_part

OPERATORS = {"LSHIFT": "<<", "RSHIFT": ">>", "OR": "|", "AND": "&"}
NUM_PATTERN = r"^(\d+) -> (\w+)"
BITMASK_UINT32 = 0xFFFFFFFF


def _init_data(lines):
    to_remove, numbers = zip(
        *[
            (i, re.match(NUM_PATTERN, line).groups())
            for i, line in enumerate(lines)
            if re.match(NUM_PATTERN, line) is not None
        ]
    )
    [lines.pop(i) for i in sorted(to_remove, reverse=True)]
    return {var: int(num) for num, var in numbers}


def get_a(data: dict[str, int], lines: list[str]):
    while "a" not in data:
        to_remove = []
        for i, line in enumerate(lines):
            if (
                var_match := re.search(rf"(\w+) (.*) (\w+) -> (\w+)", line)
            ) is not None:
                var, command, operand, next_var = var_match.groups()
                var = int(var) if var.isdigit() else data.get(var)
                operand = int(operand) if operand.isdigit() else data.get(operand)
                if (var is not None) and (operand is not None):
                    data[next_var] = (
                        eval(f"{var} {OPERATORS[command]} {operand}") & BITMASK_UINT32
                    )
                    to_remove.append(i)
            elif (not_match := re.search(rf"^NOT (.*) -> (\w+)", line)) is not None:
                operand, next_var = not_match.groups()
                if operand in data:
                    data[next_var] = ~data[operand] & BITMASK_UINT32
                    to_remove.append(i)
            elif (assignment := re.search(r"^(\w+) -> a", line)) is not None and (
                var := assignment.group(1)
            ) in data:
                data["a"] = data[var]
                to_remove.append(i)

        [lines.pop(i) for i in sorted(to_remove, reverse=True)]

    return data["a"]


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)
    data = _init_data(lines)

    if part == 1:
        print_ans(get_a(data, lines), 46065)
    else:
        data["b"] = get_a(data.copy(), lines.copy())
        print_ans(get_a(data, lines), 14134)


if __name__ == "__main__":
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
