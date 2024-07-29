from __future__ import annotations

from functools import cache

from tools import range_ops

from condition import MAX_VAL, MIN_VAL, Condition
from xmas import Xmas


class Workflow:
    def __init__(self, name: str, instructions: str = ""):
        self.name = name

        if instructions:
            self.rules = instructions.split(",")
            self.next_conds, self.next_wfs = zip(
                *[self.__parse_rule(rule) for rule in self.rules]
            )

            # reduction of workflows with all As or all Rs
            if len(res := set(self.next_wfs)) <= 1:
                self.next_conds = (None,)
                self.next_wfs = (res.pop(),)
                self.rules = self.next_wfs[0]

            if self.next_wfs.count("A") > 1:
                j = 0
                self.rules, self.next_wfs = zip(
                    *[
                        (r, n) if n != "A" else (f"{r}{(j:=j+1)}", f"A{j}")
                        for r, n in zip(self.rules, self.next_wfs)
                    ]
                )

        self.entries = self.default_ranges()
        self.winning_entry = self.default_ranges()

    @staticmethod
    def __parse_rule(rule: str) -> tuple[Condition | None, str]:
        if len(split_rule := rule.split(":")) > 1:
            crule, next_wf = split_rule
            return Condition(crule), next_wf
        else:
            return None, rule

    @staticmethod
    def default_ranges() -> dict[str, range]:
        default_range = range(MIN_VAL, MAX_VAL + 1)
        return {k: default_range for k in "xmas"}

    @staticmethod
    def get_xmas_ranges(conds: Condition | list[Condition]) -> dict[str, range]:
        ranges = Workflow.default_ranges()

        def __update_with_new_condition(new_cond: Condition):
            att, new_range = new_cond.c_range
            old_range = ranges[att]
            if range_ops.intersect(old_range, new_range):
                ranges[att] = range_ops.get_overlap(old_range, new_range)
            else:
                assert NotImplementedError, f"{att=}, {old_range=}, {new_range=}"

        if isinstance(conds, Condition):
            __update_with_new_condition(conds)
        else:
            for cond in conds:
                __update_with_new_condition(cond)

        return ranges

    @cache
    def get_chain_of_conditions_till(self, wf2_name: str) -> list[Condition]:
        wf2_index = self.next_wfs.index(wf2_name)

        next_conds = list(self.next_conds[: wf2_index + 1])
        if (N := len(next_conds)) > 1:
            next_conds[: N - 1] = [cond.inverted for cond in next_conds[: N - 1]]
        if next_conds[-1] is None:
            next_conds.pop(-1)
        return next_conds

    def __repr__(self) -> str:
        desc = self.name

        if self.rules:
            desc += "\tRULES["
            desc += ", ".join(self.rules)
            desc += "]"

        return desc

    def next_wf(self, part: Xmas) -> str:
        next_wf_ = None
        for rule in self.rules:
            condition, next_wf_ = self.__parse_rule(rule)
            if condition is not None and part.satisfies(condition):
                return next_wf_
        return next_wf_


class Path:
    def __init__(self, *wf_names):
        self.__names = wf_names
        self.__n = len(wf_names)

    def __repr__(self) -> str:
        return "/".join(self.__names)

    def __iter__(self):
        return iter(self.__names)

    def __getitem__(self, i: int) -> str:
        return self.__names[i]

    def __len__(self):
        return self.__n

    def __hash__(self) -> hash:
        return hash(str(self))

    def __lt__(self, other: Path) -> bool:
        return str(self) < str(other)

    def __eq__(self, other: Path):
        return str(self) == str(other)

    def get_conditions(self, workflows: dict[str, Workflow]) -> list[Condition]:
        conditions_ = []
        for i in range(self.__n - 1):
            wf1, wf2 = self[i], self[i + 1]
            conditions_ += workflows[wf1].get_chain_of_conditions_till(wf2)
        return conditions_
