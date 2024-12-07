from __future__ import annotations

import math
from enum import StrEnum
from typing import NamedTuple

from tools import get_numbers, parse_lines, print_ans, print_part

Operands = tuple[int, ...]


class Equation(NamedTuple):
    result: int
    operands: Operands


class Node:
    class Operation(StrEnum):
        ADD = "+"
        MULT = "*"
        CONC = ""

    def __init__(self, value: int, depth: int, part: int):
        self.value = value
        self.depth = depth

        self.children: dict[Node.Operation, Node | None]
        if part == 1:
            self.children = dict.fromkeys((Node.Operation.ADD, Node.Operation.MULT))
        else:
            self.children = dict.fromkeys(Node.Operation)

    def __repr__(self):
        return f"depth={self.depth} value={self.value}"


def dfs(result: int, operands: Operands, part: int) -> bool:
    root = Node(operands[0], depth=0, part=part)
    nodes_to_check = [root]
    final_depth = len(operands) - 1

    while nodes_to_check:
        n = nodes_to_check.pop()
        if (depth := n.depth + 1) > final_depth:
            continue

        next_operand = operands[depth]

        for operation in n.children.keys():
            node_val = eval(f"{n.value}{operation.value}{next_operand}")

            if node_val > result:
                continue

            n.children[operation] = Node(node_val, depth, part)
            if depth != final_depth:
                nodes_to_check.append(n.children[operation])
            elif node_val == result:
                return True


def prelim_search(result: int, operands: Operands, part: int) -> bool:
    if part == 1:
        return result in (sum(list(operands)), math.prod(operands))
    else:
        all_concat = int("".join(map(str, operands))) == result
        return all_concat


@print_part
def solve(filepath: str, part: int, prev_eqns: set[Equation] = None) -> set[Equation]:
    prev_eqns = prev_eqns if prev_eqns else set()

    def _is_plausible(equation: Equation) -> bool:
        res, operands = equation
        return prelim_search(res, operands, part) or dfs(res, operands, part)

    all_eqns = set(
        Equation(res, tuple(nums))
        for res, *nums in map(get_numbers, parse_lines(filepath))
    )
    prev_eqns |= set(filter(_is_plausible, all_eqns - prev_eqns))
    ans = sum(eqn.result for eqn in prev_eqns)
    if part == 1:
        print_ans(ans, correct_ans=4998764814652)
        return prev_eqns
    else:
        print_ans(ans, correct_ans=37598910447546)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    p1 = solve(FILEPATH, part=1)
    solve(FILEPATH, part=2, prev_eqns=p1)
