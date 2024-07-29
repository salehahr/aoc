from __future__ import annotations

import re

MIN_VAL = 1
MAX_VAL = 4000


class Condition:
    def __init__(self, rule: str):
        self.__rule = rule

    @property
    def c_range(self) -> tuple[str, range]:
        att_, sym, val = re.match(r"(.)([<>=]+)(\d+)", self.__rule).groups()

        match sym:
            case "<=":
                new_range = range(MIN_VAL, int(val) + 1)
            case "<":
                new_range = range(MIN_VAL, int(val))
            case ">=":
                new_range = range(int(val), MAX_VAL + 1)
            case ">":
                new_range = range(int(val) + 1, MAX_VAL + 1)
            case _:
                raise ValueError(f"{att_=}, {sym=}, {val=}")
        return att_, new_range

    @property
    def inverted(self) -> Condition:
        rule = self.__rule
        if "<" in rule:
            return Condition(rule.replace("<", ">="))
        elif ">" in rule:
            return Condition(rule.replace(">", "<="))
        else:
            raise ValueError
