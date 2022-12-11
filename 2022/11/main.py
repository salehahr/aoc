import re
from typing import Callable, Optional

from tools import parse_lines, print_part

Info = int | list[int] | Callable
Monkey = dict[str, Info]
Monkeys = dict[int, Monkey]


def parse_monkeys(filepath: str) -> Monkeys:
    monkeys: Monkeys = dict()
    set_monkey: Callable = callable
    id_: int

    def monkey_setter(id__: int) -> Callable[[str, Info, Optional[int]], None]:
        monkey = monkeys[id__]

        def set_attribute(key: str, value: Info, pos: Optional[int] = None) -> None:
            if pos is not None:
                monkey[key][pos] = value
            else:
                monkey[key] = value

        return set_attribute

    for line in parse_lines(filepath):
        if not line:
            continue

        if monkey_match := re.match(r"Monkey (\d+)", line):
            id_ = int(monkey_match.group(1))
            monkeys[id_] = {
                "items": [],
                "operation": None,
                "div": 0,
                "next": [None, None],
                "num_inspect": 0,
            }
            set_monkey = monkey_setter(id_)
        elif items_match := re.match(r"Starting items: (.*)", line):
            set_monkey("items", eval(f"[{items_match.group(1)}]"))
        elif div_by_match := re.match(r"Test: divisible by (\d+)", line):
            set_monkey("div", int(div_by_match.group(1)))
        elif operation_match := re.match(r".* new = (.*)", line):
            set_monkey(
                "operation",
                lambda old, match_group=f"{operation_match.group(1)}": eval(
                    match_group
                ),
            )
        elif next_match := re.match(r".* throw to .* (\d+)", line):
            # noinspection PyArgumentList
            set_monkey("next", int(next_match.group(1)), pos=1 if "true" in line else 0)

    return monkeys


def calc_divisor(monkeys: Monkeys, part: int) -> int:
    if part == 1:
        return 3

    divisor = 1
    for d in [mk["div"] for mk in monkeys.values()]:
        divisor *= d

    return divisor


def inspect(monkey: Monkey, item: int, part: int, mod_divisor: int):
    worry = calc_worry(monkey, item, part, mod_divisor)
    monkey["num_inspect"] += 1
    return worry, get_next(monkey, worry)


def calc_worry(monkey: Monkey, item: int, part: int, divisor: int) -> int:
    worry = monkey["operation"](item)
    if part == 1:
        return worry // divisor
    else:
        return worry % divisor


def get_next(monkey: Monkey, worry: int) -> int:
    test_result = worry % monkey["div"] == 0
    return monkey["next"][test_result]


def throw_from_to(current: Monkey, next_: Monkey, item: int) -> None:
    current["items"].pop(0)
    next_["items"].append(item)


@print_part
def solve(filepath: str, part: int = 1):
    monkeys = parse_monkeys(filepath)

    ROUNDS = 20 if part == 1 else 10000
    NUM_MONKEYS = len(monkeys)
    divisor = calc_divisor(monkeys, part)

    for _ in range(1, ROUNDS + 1):
        for id_ in range(NUM_MONKEYS):
            monkey = monkeys[id_]

            for item in monkey["items"].copy():
                worry, next_id = inspect(monkey, item, part, divisor)
                next_monkey = monkeys[next_id]
                throw_from_to(monkey, next_monkey, worry)

    inspections = [mk["num_inspect"] for mk in monkeys.values()]
    inspections.sort(reverse=True)

    print(inspections[0] * inspections[1])


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
