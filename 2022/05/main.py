import re

import context

from tools import parse_lines, print_part

Stacks = dict[int, list[chr]]

BOX_PATTERN = r"[A-Z]"
MOVE_PATTERN = r"move (\d+) from (\d+) to (\d+)"

START_POS, END_POS = 1, 9
IDX_TO_XPOS = {1 + (x - 1) * 4: x for x in range(START_POS, END_POS + 1)}


def init_stacks(lines: list[str]) -> Stacks:
    """
    Inits stacks from input data and removes lines containing stack data.
    """
    stacks = {k: [] for k in range(START_POS, END_POS + 1)}

    for i, line in enumerate(lines):
        boxes = re.findall(BOX_PATTERN, line)
        if boxes:
            line = [c for c in line]
            indices = [get_pos(line, b) for b in boxes]
            [stacks[idx].append(b) for idx, b in zip(indices, boxes)]
        else:
            lines = lines[i:]
            break

    for v in stacks.values():
        v.reverse()

    return stacks


def get_pos(line: list[str], substring: chr) -> int:
    """
    Returns position of the box.
    """
    index = line.index(substring)
    line[index] = "_"
    return IDX_TO_XPOS[index]


def move(command: list[str], stacks: Stacks, part: int):
    """
    Moves boxes to another stack based on the given command.
    """
    num_boxes, pos0, posN = [int(x) for x in command.groups()]

    popped = [stacks[pos0].pop() for _ in range(num_boxes)]

    if part == 2:
        popped.reverse()

    stacks[posN] += popped


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath, strip=False)
    stacks = init_stacks(lines)

    for line in lines:
        move_command = re.match(MOVE_PATTERN, line)

        if move_command:
            move(move_command, stacks, part)

    result = "".join([v[-1] for k, v in stacks.items()])
    print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
