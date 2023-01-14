import re
from typing import NamedTuple

from tools import manhattan_distance, parse_lines, print_ans, print_part

PATTERN = r".*x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)"


class Sensor(NamedTuple):
    x: int
    y: int
    range: int


class Beacon(NamedTuple):
    x: int
    y: int


def _map_coords(line: str) -> tuple[Sensor, Beacon]:
    xs, ys, xb, yb = tuple(map(int, re.match(PATTERN, line).groups()))
    dist = manhattan_distance(xs, ys, xb, yb)
    return Sensor(xs, ys, dist), Beacon(xb, yb)


def get_perimeter(sensor, max_c):
    radius = sensor.range + 1
    perimeter = list()
    for r in range(radius + 1):
        diff = radius - r
        coords = {(r, -diff), (r, diff), (-r, -diff), (-r, diff)}
        perimeter += [(sensor.x + x, sensor.y + y) for x, y in coords]
    assert len(perimeter) == radius * 4
    return [(x, y) for x, y in perimeter if 0 <= x <= max_c and 0 <= y <= max_c]


def point_in_range(point, sensor):
    dist_to_point = manhattan_distance(*point, sensor.x, sensor.y)
    return dist_to_point <= sensor.range


@print_part
def solve(filepath: str, part: int = 1):
    sensors, beacons = zip(*map(_map_coords, parse_lines(filepath)))

    if part == 1:
        if "short" in filepath:
            ROW, CORRECT_ANS = 10, 26
        else:
            ROW, CORRECT_ANS = 2_000_000, 4_725_496
        columns = set()
        for sensor in sensors:
            dist_vertical = manhattan_distance(sensor.x, sensor.y, sensor.x, ROW)
            if (diff := sensor.range - dist_vertical) >= 0:
                columns |= set(range(sensor.x - diff, sensor.x + diff + 1))
        columns -= set([b.x for b in beacons if b.y == ROW])
        print_ans(len(columns), CORRECT_ANS)
    else:
        if "short" in filepath:
            MAX_C, CORRECT_ANS = 20, 56_000_011
        else:
            MAX_C, CORRECT_ANS = 4_000_000, 12_051_287_042_458

        xy, xy_undetected = (0, 0), False
        for sensor_a in sensors:
            for xy in get_perimeter(sensor_a, MAX_C):
                for sensor_b in sensors:
                    if sensor_a == sensor_b:
                        continue
                    if point_in_range(xy, sensor_b):
                        break
                else:
                    xy_undetected = True
                    break
            if xy_undetected:
                x, y = xy
                print_ans(x * 4_000_000 + y, CORRECT_ANS)
                break


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
