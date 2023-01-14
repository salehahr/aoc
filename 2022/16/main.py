from __future__ import annotations

import re
from collections import UserDict
from dataclasses import dataclass
from typing import NamedTuple, Optional

from tools import parse_lines, print_part

TIME_TO_OPEN = 1
PATTERN = r"Valve (\w+).*rate=(\d+);.*valves? (.*)"


class Valves(UserDict):
    def __init__(self, valve_list: list[name, ValveData]):
        super().__init__()

        self.data = {name: data for name, data in valve_list}
        self.targets: set[str] = {
            v for v, data in self.data.items() if data.pressure > 0 or v == "AA"
        }

        self.time_from_to = dict()
        self._init_times()

    def _init_times(self):
        for start_ in self.targets:
            seen = set()
            seen.add(start_)

            to_visit = self.data[start_].flows_to

            distance = 0
            distances = {start_: distance}
            while len(to_visit) > 0:
                distance += 1
                distances |= {v: distance for v in to_visit if v in self.targets}
                seen |= set(to_visit)
                to_visit = (
                    set().union(*[self.data[v].flows_to for v in to_visit]) - seen
                )

            for next_, distance in distances.items():
                self.time_from_to[start_, next_] = distance

    def traverse(
        self,
        time_max: int,
        pressures_dict: dict,
        valve: str = "AA",
        pressure: int = 0,
        now: int = 0,
        seen: frozenset[str] = frozenset(),
        do_print: bool = False,
    ) -> dict[frozenset, int]:
        unseen_targets = self.targets - seen
        for target in unseen_targets:
            time_new = now + self.time_from_to[valve, target] + TIME_TO_OPEN

            if time_new < time_max:
                new_seen = set(seen)
                new_seen.add(target)
                new_seen = frozenset(new_seen)

                time_remaining = time_max - time_new
                new_pressure = pressure + (self.data[target].pressure * time_remaining)
                if new_seen in pressures_dict:
                    pressures_dict[new_seen] = max(
                        pressures_dict[new_seen], new_pressure
                    )
                else:
                    pressures_dict[new_seen] = new_pressure

                self.traverse(
                    time_max,
                    pressures_dict,
                    valve=target,
                    pressure=new_pressure,
                    now=time_new,
                    seen=new_seen,
                )

        if do_print:
            print(max(pressures_dict.values()))

        return pressures_dict


def parse_data(line: str):
    name, pressure, flows_to = re.match(PATTERN, line).groups()
    return name, ValveData(int(pressure), set([_.strip() for _ in flows_to.split(",")]))


class ValveData(NamedTuple):
    pressure: int
    flows_to: set[str]


@print_part
def solve(filepath: str, part: int = 1):
    data = [parse_data(line) for line in parse_lines(filepath)]
    valves = Valves(data)
    max_time = 30 if part == 1 else 26

    if part == 1:
        valves.traverse(max_time, pressures_dict=dict(), do_print=True)
    else:
        pressures_dict = valves.traverse(max_time, pressures_dict=dict())
        max_pressure = max(pressures_dict.values())
        for i, (seen, pressure) in enumerate(pressures_dict.items()):
            for seen_e, pressure_e in list(pressures_dict.items())[i + 1 :]:
                if seen.isdisjoint(seen_e) and (pressure + pressure_e > max_pressure):
                    max_pressure = pressure + pressure_e
        print(max_pressure)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
