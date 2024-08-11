import math
from collections import deque

from tools import print_part

from module import get_modules


def push_button(
    modules, period: int = None, l3_cycles: dict = None
) -> list[int] | None:
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

        if l3_cycles and module.name in l3_cycles.keys():
            if module.state == 1 and l3_cycles[module.name] is None:
                l3_cycles[module.name] = period

                if all(l3_cycles):
                    return

        to_process += [(next_name, name) for next_name in module.out]

    return low_high


def get_prev_module_names(current_modules: str | list, modules: dict) -> list:
    def __prev_mod_name_of_one_module(cm_: str) -> list:
        return [x.name for x in filter(lambda x: cm_ in x.out, modules.values())]

    if isinstance(current_modules, str):
        return __prev_mod_name_of_one_module(current_modules)
    else:
        mod_names = []
        for cm in current_modules:
            mod_names += __prev_mod_name_of_one_module(cm)
        return mod_names


@print_part
def solve(filepath: str, part: int):

    MODULES = get_modules(filepath)
    period = 0

    if part == 1:
        cumulative_lh = [0, 0]
        MAX_PRESSES_P1 = 1000

        while True:
            period += 1
            lh_pulses = push_button(MODULES)

            cumulative_lh[0] += lh_pulses[0]
            cumulative_lh[1] += lh_pulses[1]
            if period == MAX_PRESSES_P1:
                return math.prod(cumulative_lh)
    else:
        LAST_MODULE = "rx"  # (out LOW)

        # L1 - rm             (out LOW)
        L1_MODULES = get_prev_module_names(LAST_MODULE, MODULES)

        # L2 - dh, qd, bb, dp (all out HIGH)
        L2_MODULES = get_prev_module_names(L1_MODULES, MODULES)

        # L3 - dt, xm, vt, gr (all out LOW)
        L3_MODULES = get_prev_module_names(L2_MODULES, MODULES)

        l3_cycles = dict.fromkeys(L3_MODULES, None)

        while True:
            period += 1
            push_button(MODULES, period, l3_cycles=l3_cycles)

            if all(l3_cycles.values()):
                return math.lcm(*l3_cycles.values())


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
