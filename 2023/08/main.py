import itertools
import math
import re

from tools import parse_lines, print_part


def get_data(filepath: str) -> tuple[list[bool], dict[str, tuple[str, str]]]:
    steps_, _, *next_nodes = parse_lines(filepath)

    steps = [step == "R" for step in steps_]

    map_next_nodes = dict()
    for rule in next_nodes:
        node, next_left, next_right = re.match(r"(\w+) = .(\w+), (\w+)", rule).groups()
        map_next_nodes[node] = (next_left, next_right)

    return steps, map_next_nodes


def is_final_node(node: str, part: int):
    return node == "ZZZ" if part == 1 else node.endswith("Z")


def is_start_node(node: str, part: int):
    return node == "AAA" if part == 1 else node.endswith("A")


@print_part
def solve(filepath: str, part: int):
    steps, next_nodes = get_data(filepath)

    initial_nodes = [node for node in next_nodes.keys() if is_start_node(node, part)]
    num_steps = [0] * len(initial_nodes)

    for i, node0 in enumerate(initial_nodes):
        looped_steps = itertools.cycle(steps)
        node = node0
        while not is_final_node(node, part):
            num_steps[i] += 1
            node = next_nodes[node][next(looped_steps)]

    print(math.lcm(*num_steps))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
