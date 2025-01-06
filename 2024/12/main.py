from dataclasses import dataclass
from typing import ClassVar

from tools import get_array, print_ans, print_part
from tools.generic_types import Coordinates, Direction, get_neighbours


@dataclass
class Region:
    SHAPE: ClassVar
    PART: ClassVar

    item: str
    data: set[Coordinates]

    area: int = None

    def __post_init__(self):
        self.area = len(self.data)

        outside_rcs = filter(
            lambda rc: len(self._neighbours_in_region(rc)) < 4, self.data
        )
        self.perimeter = sum(
            map(lambda rc: 4 - len(self._neighbours_in_region(rc)), outside_rcs)
        )

    def _neighbours_in_region(self, coord: Coordinates) -> set[Coordinates]:
        return set(get_neighbours(coord, *self.SHAPE)) & self.data

    @property
    def price(self) -> int:
        if self.PART == 1:
            return self.area * self.perimeter


def is_neighbour(c1: Coordinates, c2: Coordinates) -> bool:
    return (c2 - c1) in Direction


def extract_region(
    coord0: Coordinates, same_plant_coords: set[Coordinates]
) -> set[Coordinates]:
    region = {coord0}
    to_explore = {coord0}
    while to_explore:
        coord = to_explore.pop()
        to_explore |= set(filter(lambda cr: is_neighbour(coord, cr), same_plant_coords))
        region |= to_explore
        same_plant_coords -= to_explore
    return region


@print_part
def solve(filepath: str, part: int = 1):
    garden = get_array(filepath)
    h, w = garden.shape
    Region.SHAPE = garden.shape
    Region.PART = part

    all_coords = {Coordinates(row, col) for row in range(h) for col in range(w)}
    plants = {garden[i] for i in all_coords}
    regions: list[Region] = []

    for plant in plants:
        same_plant_coords = set(filter(lambda rc: garden[rc] == plant, all_coords))
        while same_plant_coords:
            coord0 = same_plant_coords.pop()
            region = extract_region(coord0, same_plant_coords)
            regions.append(Region(plant, region))

    print_ans(sum(r.price for r in regions), correct_ans=1371306)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    # solve(FILEPATH, part=2)
