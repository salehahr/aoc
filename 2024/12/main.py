from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import numpy as np

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, Direction, get_neighbours


class Region:
    MAX_MAP_DIMS: tuple[int, int]

    def __init__(
        self,
        name: str,
        coords: Iterable[Coordinates],
        outer_coords: set[Coordinates] = None,
    ):
        self.name = name
        self.data = set(coords)
        self.outer_coords = outer_coords

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self):
        return f"Region {self.name}: " f"AREA {self.area} x PERIMETER {self.perimeter}"

    @classmethod
    def get_subregions(
        cls, name: str, coords: Iterable[Coordinates]
    ) -> tuple[Region, ...]:
        all_coords = set(coords)
        subregions: list[Region] = []

        while all_coords:
            subregion = cls.__extract_subregion(name, all_coords)
            subregions.append(subregion)
            all_coords -= subregion.data

        return tuple(subregions)

    @classmethod
    def __extract_subregion(
        cls, name: str, matching_plants: set[Coordinates]
    ) -> Region:
        point = matching_plants.pop()
        matching_plants.add(point)

        subregion = {point}
        outer_coords = set()

        seen = set()
        points_to_check = {point}
        while points_to_check:
            point_to_check = points_to_check.pop()
            seen.add(point_to_check)

            orth_neighbours = cls.neighbours(point_to_check, all_coords=matching_plants)
            diag_neighbours = cls.neighbours(
                point_to_check, all_coords=matching_plants, diags=True
            )
            if len(orth_neighbours) != 4:  # is outer coord
                outer_coords.add(point_to_check)
            elif len(diag_neighbours) != 8:
                outer_coords.add(point_to_check)

            points_to_check |= orth_neighbours - seen
            subregion |= orth_neighbours

        return cls(name, subregion, outer_coords=outer_coords)

    @property
    def area(self) -> int:
        return len(self)

    @property
    def n_sides(self) -> int:
        n_corners = 0
        for p in self.outer_coords:
            orth_neighbours = self.neighbours(p, all_coords=self.data)
            match len(orth_neighbours):
                case 0:
                    return 4
                case 1:
                    """
                     p
                    ono
                    """
                    n_corners += 2
                case 2:
                    """
                    Covers the case (both horz. and vert.):
                    oonpnoo  → no corners at p

                    The following case is covered by case 3 for each node n:
                    ooo ooo
                    oonpnoo  → 2 corners at p
                    """
                    dir1, dir2 = (Direction(n - p) for n in orth_neighbours)
                    if dir1.category != dir2.category:
                        """
                        onp  onp
                        ofn  o n
                        ooo  o o
                        """
                        filler = p + dir1 + dir2
                        if filler in self.data:
                            n_corners += 1
                        else:
                            n_corners += 2
                case 3:
                    """
                    →→→  long dir
                    npn  ↓
                    fnf  ↓ short dir
                    """
                    dirs = defaultdict(list)
                    long_dir = None
                    for neighbour in orth_neighbours:
                        d = Direction(neighbour - p).category
                        if dirs[d]:
                            long_dir = d
                        dirs[d].append(neighbour)
                    short_dir = long_dir.opposite
                    short_n = dirs[short_dir][0]
                    fillers = {short_n + d for d in long_dir.value}
                    n = 2 - len(fillers & self.data)
                    n_corners += n
                case 4:
                    """
                    1 diag neighbour → p has 3 corners:
                    ooo
                    oon
                    onpn
                      n

                    0 diag neighbours → p has 4 corners:
                     n
                    npn
                     n
                    """
                    diag_neighbours = (
                        self.neighbours(p, self.data, diags=True) - orth_neighbours
                    )
                    n = 4 - len(diag_neighbours)
                    n_corners += n

        return n_corners

    @property
    def perimeter(self) -> int:
        return sum(
            map(lambda rc: 4 - len(self.neighbours(rc, self.data)), self.outer_coords)
        )

    @property
    def price_p1(self) -> int:
        return self.area * self.perimeter

    @property
    def price_p2(self) -> int:
        return self.area * self.n_sides

    @classmethod
    def neighbours(
        cls, rc: Coordinates, all_coords: set[Coordinates], diags: bool = False
    ) -> set[Coordinates]:
        return set(get_neighbours(rc, *cls.MAX_MAP_DIMS, diags)) & all_coords


@print_part
def solve(filepath: str, part: int = 1):
    map_ = get_array(filepath)
    Region.MAX_MAP_DIMS = map_.shape

    price = 0
    for plant in set(str(rc) for r in map_ for rc in r):
        coordinates = (Coordinates(*map(int, rc)) for rc in np.argwhere(map_ == plant))
        subregions = Region.get_subregions(plant, coordinates)
        price += sum(getattr(subregion, f"price_p{part}") for subregion in subregions)

    correct_ans = 1371306 if part == 1 else 805880
    print_ans(price, correct_ans)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
