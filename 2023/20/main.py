import math
from collections import deque

from module import get_modules
from tools import print_part
from tools.generic_types import Coordinates


def push_button(modules):
    name0, prev_name0 = "broadcaster", "button"
    to_process = deque([(name0, prev_name0)])

    low_high = [0, 0]

    while to_process:
        name, prev_name = to_process.popleft()
        module, prev_module = modules[name], modules[prev_name]

        pulse = prev_module.output
        low_high[pulse] += 1

        if not module.process(prev_name):
            continue

        to_process += [(next_name, name) for next_name in module.out]

    return low_high


def cumulative_lh(cycle: int, hist: list[Coordinates]) -> Coordinates:
    if cycle == 0:
        return Coordinates(0, 0)
    lows, highs = map(sum, zip(*hist[:cycle]))
    return Coordinates(lows, highs)


@print_part
def solve(filepath: str, part: int):
    modules = get_modules(filepath)

    def cycle_found() -> bool:
        states = [int(o.state) for o in modules.values() if not o.is_generic]
        states_str = "".join([str(s) for s in states])
        states_bin = int(states_str, 2)

        return states_bin == 0

    max_presses = 1000
    hist = []
    period = 0

    # part 2
    # [&st, &tn, &hh, &dt] -> &lv -> rx
    lv_inp = modules["lv"].inp
    print([modules[x] for x in lv_inp])

    while True:
        period += 1
        delta_lh = push_button(modules)
        hist.append(Coordinates(*delta_lh))

        if part == 1:
            if period == max_presses or cycle_found():
                n, rem = max_presses // period, max_presses % period
                lh = n * cumulative_lh(period, hist) + cumulative_lh(rem, hist)
                return math.prod(lh)
        elif part == 2:
            if period == max_presses:
                print("debug")
                print(f"{period=}")
                break


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
