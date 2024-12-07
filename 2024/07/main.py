from __future__ import annotations

import math
from enum import StrEnum

from tools import get_numbers, parse_lines, print_ans


class Operation(StrEnum):
    ADD = "+"
    MULT = "*"
    CONC = ""


class Node:
    def __init__(self, value: int, depth: int, part: int):
        self.value = value
        self.depth = depth

        self.children: dict[Operation, Node | None]
        if part == 1:
            self.children = dict.fromkeys((Operation.ADD, Operation.MULT))
        else:
            self.children = dict.fromkeys(Operation)

    def __repr__(self):
        return f"depth={self.depth} value={self.value}"


def dfs(result: int, operands: list[int], part: int) -> bool:
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


def prelim_search(result: int, operands: list[int], part: int) -> bool:
    if part == 1:
        return result in (sum(operands), math.prod(operands))
    else:
        all_concat = int("".join(map(str, operands))) == result
        return all_concat


def solve(filepath: str):
    total_result = 0

    p1_results = []
    all_eqns = {res: nums for res, *nums in (get_numbers(line) for line in parse_lines(filepath))}
    part = 1
    for result, operands in all_eqns.items():
        if prelim_search(result, operands, part) or dfs(result, operands, part):
            p1_results.append(result)
            total_result += result
    print_ans(total_result)  #, correct_ans=1430271835320)

    p2_results = []
    p2_eqns = {res: nums for res, nums in all_eqns.items() if res not in p1_results}
    part = 2
    for result, operands in p2_eqns.items():
        if prelim_search(result, operands, part) or dfs(result, operands, part):
            p2_results.append(result)
            total_result += result
    print_ans(total_result)

    p3_eqns = {res: nums for res, nums in all_eqns.items() if res not in (p1_results + p2_results)}
    for eqn in p3_eqns.items():
        print(eqn)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input_sar.txt"  # 456565678642322 too low, 456565678667482 correct, diff 25160

    solve(FILEPATH)
