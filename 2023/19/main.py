import math
import re

from tools import parse_lines, print_ans, print_part

from workflow import Path, Workflow
from xmas import Xmas

Parts = list[Xmas]
Workflows = dict[str, Workflow]


def get_workflows(lines: list[str]) -> tuple[Workflows, Parts]:
    wf_parts_sep_index = lines.index("")
    workflows = dict()

    for wf in lines[:wf_parts_sep_index]:
        name, instructions = re.findall(r"(^\w+){(.*)}", wf)[0]
        workflows[name] = Workflow(name, instructions)

    parts_str = lines[wf_parts_sep_index + 1 :]
    parts = [
        Xmas(*map(int, re.findall(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)", part)[0]))
        for part in parts_str
    ]

    return workflows, parts


def successful_paths(workflows: Workflows) -> set[Path]:
    paths_to_check = {Path("in")}
    paths_ok = set()

    while paths_to_check:
        path = paths_to_check.pop()
        end_wf = path[-1]
        for next_wf in workflows[end_wf].next_wfs:
            next_path = Path(*path, next_wf)
            if next_wf.startswith("A"):
                paths_ok.add(next_path)
            elif next_wf != "R":
                paths_to_check.add(next_path)

    return paths_ok


@print_part
def solve(filepath: str, part: int):
    lines = parse_lines(filepath)
    workflows, parts = get_workflows(lines)

    if part == 1:
        wf0, sum_ratings = "in", 0
        for xmas_part in parts:
            name = wf0
            while not (name.startswith("R") or name.startswith("A")):
                if (name := workflows[name].next_wf(xmas_part)).startswith("A"):
                    sum_ratings += xmas_part.rating

        correct_ans = {
            "input.txt": 432427,
            "input_short.txt": 19114,
            "input_r1.txt": 12163,
        }
        print_ans(sum_ratings, correct_ans[filepath])
    else:
        num_combinations = 0
        for path in successful_paths(workflows):
            conditions = path.get_conditions(workflows)
            xmas_ranges = Workflow.get_xmas_ranges(conditions)
            num_combinations += math.prod(
                (v.stop - v.start) for v in xmas_ranges.values()
            )

        correct_ans = {
            "input.txt": 143760172569135,
            "input_short.txt": 167409079868000,
            "input_r1.txt": 132753196000000,
        }
        print_ans(num_combinations, correct_ans[filepath])


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    # FILEPATH = "input_r1.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
