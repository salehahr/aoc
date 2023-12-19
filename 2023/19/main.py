import re
from collections import defaultdict
from typing import NamedTuple

from tools import parse_lines, print_part, range_ops


class Xmas(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    def __repr__(self):
        return repr(tuple(self))

    @property
    def rating(self):
        return sum([self.__getattribute__(x) for x in "xmas"])


def next_workflow(rule: str):
    if len(split_rule := rule.split(":")) > 1:
        condition, next_wf = split_rule
    else:
        condition, next_wf = None, rule
    return condition, next_wf


def solve_part1(lines, split_index):
    workflows = get_workflows(lines, split_index)
    parts_str = lines[split_index + 1 :]

    def __next_workflow(xmas: Xmas, prev_workflow: str) -> str:
        for rule in workflows[prev_workflow]["rules"]:
            condition, next_wf = next_workflow(rule)
            if condition and eval("xmas." + condition):
                return next_wf
        return next_wf

    workflow0, ratings = "in", 0
    for part_str in parts_str:
        xmas = Xmas(
            *map(int, re.findall(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)", part_str)[0])
        )
        workflow = workflow0
        while workflow not in "RA":
            if (workflow := __next_workflow(xmas, workflow)) == "A":
                ratings += xmas.rating

    print(ratings)


def __default_ranges():
    default_range = range(1, 4000 + 1)
    return {k: default_range for k in "xmas"}


def get_workflows(lines: list[str], split_index: int):
    workflows = defaultdict(lambda: {"rules": [], "entries": __default_ranges()})

    for wf in lines[:split_index]:
        name, instructions = re.findall(r"(^\w+)\{(.*)\}", wf)[0]
        workflows[name]["rules"] = instructions.split(",")

    return workflows


@print_part
def solve(filepath: str, part: int):
    lines = parse_lines(filepath)
    split_index = lines.index("")

    if part == 1:
        solve_part1(lines, split_index)
    else:
        workflows = get_workflows(lines, split_index)

        wf0 = "in"

        ct, break_at = 0, 1
        todos = [wf0]

        while todos:
            wf = todos.pop(0)
            entries_current = {k: v for k, v in workflows[wf]["entries"].items()}

            for rule in workflows[wf]["rules"]:
                condition, next_wf = next_workflow(rule)
                todos.append(next_wf)

                if condition:
                    att, sign, num = re.findall(r"(\w)(.)(\d+)", condition)[0]
                    match sign:
                        case "<":
                            condition_range = range(1, int(num))
                            inv_condition_range = range(condition_range.stop, 4000 + 1)
                        case ">":
                            condition_range = range(int(num) + 1, 4000 + 1)
                            inv_condition_range = range(1, condition_range.start + 1)
                        case _:
                            raise NotImplementedError
                    for k in "xmas":
                        entries_next_k = workflows[next_wf]["entries"][k]
                        if att == k:
                            range_next_todo = range_ops.get_overlap(
                                entries_current[k], condition_range
                            )
                            workflows[next_wf]["entries"][k] = range_ops.get_overlap(
                                entries_next_k, range_next_todo
                            )
                            entries_current[k] = inv_condition_range
                        else:
                            overlap = range_ops.get_overlap(
                                entries_next_k, entries_current[k]
                            )
                            workflows[next_wf]["entries"][k] = overlap
                else:
                    if next_wf not in "RA":
                        for k in "xmas":
                            entries_next_k = workflows[next_wf]["entries"][k]
                            workflows[next_wf]["entries"][k] = range_ops.get_overlap(
                                entries_next_k, entries_current[k]
                            )
                    else:
                        raise NotImplementedError

            ct += 1
            if ct > break_at:
                break

        for wf0 in workflows.items():
            print(wf0)
        return

        processed_workflows = defaultdict(list)
        for name, all_rules in workflows.items():
            prev_inv_condition = None
            for rule in all_rules["rules"]:
                condition, next_wf = rule.split(":")
                match next_wf[-1]:
                    case "R":
                        pass
                    case "A":
                        pass
                    case _:
                        pass
                if prev_inv_condition:
                    new_condition = prev_inv_condition + " and " + condition
                else:
                    new_condition = condition
                print(new_condition)
                prev_inv_condition = invert_rule(condition)
            acc_rules, rej_rules, shunt_rules = partition_rule_types(all_rules)
            print(all_rules)
            print("\t", acc_rules, rej_rules, shunt_rules)
            # if not shunt_rules:
            #     acc_rules, rej_rules = summarise_acc_rules_for_workflow(acc_rules, rej_rules, all_rules["fallback"])
            #     if acc_rules is not True:
            #         processed_workflows[name] += acc_rules
            #     else:
            #         processed_workflows[name] = acc_rules

        for processed_wf_acc_rule in list(processed_workflows.items()):
            workflows.pop(processed_wf_acc_rule[0])

        # ct = 0
        # while True:
        #     for workflow in list(workflows.items()):
        #         wf, wf_all_rules = workflow
        #         print(wf, wf_all_rules)
        #         handle_processed_fallback(workflow, processed_workflows, workflows)
        #         acc_rules, rej_rules, shunt_rules = partition_rule_types(wf_all_rules)
        #         if shunt_rules:
        #             for shunt_rule in filter(lambda x: x != "fallback", shunt_rules):
        #                 shunt_condition, shunt_wf = shunt_rule.split(":")
        #                 if shunt_wf in processed_workflows.keys():
        #                     shunt_acc_rule = processed_workflows[shunt_wf]
        #                     if wf_all_rules["fallback"] == "A":
        #                         acc_rules.remove("fallback")
        #                         acc_rules += [invert_rule(rej) for rej in rej_rules]
        #                         rej_rules = []
        #                     print("\t", shunt_rule, shunt_acc_rule)
        #             print(acc_rules, rej_rules, shunt_rules)
        #     ct += 1
        #     if ct > 0:
        #         break

        print("\nProcessed")
        for processed_wf_acc_rule in list(processed_workflows.items()):
            print(processed_wf_acc_rule)

        # print("\nUnprocessed")
        # for w in workflows.items():
        #     print(w)


def handle_processed_fallback(workflow, processed_workflows, workflows):
    wf, wf_all_rules = workflow
    fallback = wf_all_rules["fallback"]
    if fallback not in processed_workflows.keys():
        return

    processed_wf_acc_rule = processed_workflows[fallback]

    acc_rules, rej_rules, shunt_rules = partition_rule_types(wf_all_rules)
    if rej_rules:
        raise NotImplementedError
    elif len(shunt_rules) > 1:
        raise NotImplementedError

    if processed_wf_acc_rule is not True:
        acc_rules += processed_wf_acc_rule
    else:
        acc_rules = True

    processed_workflows[wf] = acc_rules
    workflows.pop(wf)


def partition_rule_types(rules_and_fallback):
    rules, fallback = rules_and_fallback.values()
    acc_rules = list(
        map(
            lambda x: x.split(":")[0],
            filter(lambda x: x[-1] == "A", rules),
        )
    )
    rej_rules = list(
        map(
            lambda x: x.split(":")[0],
            filter(lambda x: x[-1] == "R", rules),
        )
    )
    shunt_rules = list(
        map(
            lambda x: x,
            filter(lambda x: x[-1] not in "RA", rules),
        )
    )

    match fallback:
        case "A":
            acc_rules.append("fallback")
        case "R":
            rej_rules.append("fallback")
        case _:
            shunt_rules.append("fallback")

    return acc_rules, rej_rules, shunt_rules


def summarise_acc_rules_for_workflow(acc_rules, rej_rules, fallback):
    match fallback:
        case "A":
            if rej_rules:
                acc_rules = [invert_rule(rule) for rule in rej_rules]
                rej_rules = []
            else:
                acc_rules = True
        case "R":
            if acc_rules:
                rej_rules = []
            else:
                rej_rules.remove("fallback")
                acc_rules = [invert_rule(rule) for rule in rej_rules]
                rej_rules = []
        case _:
            raise NotImplementedError
    return acc_rules, rej_rules


def invert_rule(rule: str):
    att, sign, num = re.findall(r"(\w)(.)(\d+)", rule)[0]
    match sign:
        case ">":
            sign = "<="
        case "<":
            sign = ">="
        case _:
            raise NotImplementedError
    return att + sign + num


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
