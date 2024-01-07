from __future__ import annotations

from dataclasses import dataclass


def compare_bricks(b1: Brick, b2: Brick):
    if b1.z.start == b2.z.start:
        if b1.z.stop == b2.z.stop:
            return 0
        else:
            return -1 if b1.z.stop < b2.z.stop else 1
    else:
        return -1 if b1.z.start < b2.z.start else 1


@dataclass
class Brick:
    id_: int
    x: range = None
    y: range = None
    z: range = None
    at_rest: bool = False
    height: int = 0
    supported_by: set = None
    supports: set = None

    def __post_init__(self):
        self.height = self.z.stop - self.z.start + 1
        self.supported_by = set()

    def at_level(self, level: int) -> bool:
        return self.z.start <= level <= self.z.stop

    def __lt__(self, other: Brick):
        if self.z.start == other.z.start:
            return self.z.stop < other.z.stop
        else:
            return self.z.start < other.z.start
