import sys
from collections import defaultdict

import range_ops
from tools import flatten_list, get_numbers, parse_lines, print_part


def seed_factory(line: str, part: int) -> list[int | range]:
    if part == 1:
        return get_numbers(line)
    else:
        nums = get_numbers(line)
        starts, lengths = nums[::2], nums[1::2]
        return [range(s, s + l) for s, l in zip(starts, lengths)]


def parse_maps(lines):
    maps = dict()
    new_dict = dict()

    for line in lines:
        if not line:
            continue

        if not line[0].isdigit():
            new_dict = dict()
            maps[line.split()[0]] = new_dict
        else:
            dest_start, src_start, length = get_numbers(line)
            dest_range = range(dest_start, dest_start + length)
            src_range = range(src_start, src_start + length)
            new_dict[src_range] = dest_range

    return maps


def slice_destination_range(src0: range, src: range, dst: range):
    """
    Returns new destination range based on overlap of src0 with src
    """
    diff_start = src0.start - src.start
    length = src0.stop - src0.start
    return range(dst.start + diff_start, dst.start + diff_start + length)


@print_part
def solve(filepath: str, part: int = 1):
    lines = parse_lines(filepath)

    seeds = seed_factory(lines[0], part=part)
    maps = parse_maps(lines[2:])

    lowest_loc = sys.maxsize

    if part == 1:
        for seed in seeds:
            src_num = seed
            for map_descr, map_ in maps.items():
                for src, dst in map_.items():
                    if src_num in src:
                        diff = src_num - src.start
                        src_num = dst.start + diff
                        break
            lowest_loc = min(lowest_loc, src_num)
    else:
        for seed_range in seeds:
            range_maps = dict()
            sources0 = [seed_range]

            for map_descr, map_ in maps.items():
                destinations0 = defaultdict(set)
                range_maps[map_descr] = destinations0

                for src0 in sources0:
                    found = False
                    overlaps = []

                    for src, dst in map_.items():
                        if not range_ops.intersect(src0, src):
                            continue

                        overlap = range_ops.get_overlap(src0, src)
                        destinations0[src0].add(
                            slice_destination_range(overlap, src, dst)
                        )

                        overlaps.append(overlap)
                        range_ops.collapse(overlaps)
                        if overlaps and overlaps[0] == src0:
                            found = True
                            break

                    if not found:
                        destinations0[src0].add(src0)

                sources0 = flatten_list(list(destinations0.values()))

                if "location" in map_descr:
                    lowest_loc = min(lowest_loc, min([r.start for r in sources0]))

    print(lowest_loc)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
