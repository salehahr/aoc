from __future__ import annotations

import abc
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from tools import parse_lines


def get_modules(filepath: str) -> dict[str, Module]:
    modules = dict()
    inputs_todo = defaultdict(set)  # list of inputs

    modules["button"] = Generic(modules, "button")

    for inp_n, outputs_n in map(lambda x: x.split(" -> "), parse_lines(filepath)):
        module = Module.create(inp_n, modules)
        modules[module.name] = module

        if module.name in inputs_todo:
            module.inp += inputs_todo[module.name]
            del inputs_todo[module.name]

        for out_n in outputs_n.split(", "):
            module.out.append(out_n)
            if out_n in modules:
                modules[out_n].inp.append(module.name)
            else:
                inputs_todo[out_n].add(module.name)

    for obj_n, inputs in inputs_todo.items():
        assert obj_n not in modules
        module = Module.create(obj_n, modules)
        modules[obj_n] = module
        module.inp += inputs

    for inverter in filter(lambda v_: isinstance(v_, Inverter), modules.values()):
        inverter.init_memory()

    return modules


@dataclass
class Module(abc.ABC):
    modules: dict
    name: str = ""
    state: bool = False
    inp: list = None
    out: list = None

    def __post_init__(self):
        self.inp = []
        self.out = []

    def __repr__(self) -> str:
        return f"{self.name}(s={int(self.state)})"

    @abc.abstractmethod
    def process(self, input_module: str) -> Optional[bool]:
        pass

    @staticmethod
    def create(name: str, modules: dict) -> Module:
        match name[0]:
            case "%":
                obj = FlipFlop(modules, name=name[1:])
            case "&":
                obj = Inverter(modules, name=name[1:])
            case "b":
                obj = Broadcaster(modules, name=name)
            case _:
                obj = Generic(modules, name=name)
        return obj

    @property
    def is_generic(self) -> bool:
        return isinstance(self, Generic)


class FlipFlop(Module):
    def process(self, input_module: str) -> Optional[bool]:
        # high pulse ignored
        if self.modules[input_module].output:
            return

        self.state = not self.state
        return True

    @property
    def output(self):
        return self.state


class Inverter(Module):
    memory: dict

    def __post_init__(self):
        super(Inverter, self).__post_init__()

    def init_memory(self):
        self.memory = dict.fromkeys(self.inp, False)

    def __repr__(self):
        return f"{self.name}(s={int(self.state)}) {self.mem_str}"

    def process(self, input_module: str) -> bool:
        self.memory[input_module] = self.modules[input_module].output
        self.state = all(self.memory.values())
        return True

    @property
    def output(self):
        return not self.state

    @property
    def mem_str(self):
        mems = [f"{i}: {int(b)}" for i, b in self.memory.items()]
        mstr = ", ".join(mems)
        return "{" + mstr + "}"


class Broadcaster(Module):
    def process(self, input_module: str) -> bool:
        self.state = self.modules[input_module].output
        return True

    @property
    def output(self):
        return self.state


class Generic(Module):
    def process(self, input_module: str) -> None:
        self.state = self.modules[input_module].output

    @property
    def output(self):
        return False
