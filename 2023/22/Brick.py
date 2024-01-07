from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Brick:
    id_: int
    x: range = None
    y: range = None
    z: range = None
    at_rest: bool = False
    height: int = 0
    supported_by: set = None

    def __post_init__(self):
        self.height = self.z.stop - self.z.start
        self.supported_by = set()

    def __lt__(self, other: Brick):
        if self.z.start == other.z.start:
            return self.z.stop < other.z.stop
        else:
            return self.z.start < other.z.start
