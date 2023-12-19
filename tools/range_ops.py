def get_overlap(src0: range, src: range):
    if src0 == src:  # exact
        return src
    elif r1_inside_r2(src0, src):  # smaller
        return src0
    elif r1_inside_r2(src, src0):  # bigger
        return src

    if src0.start <= src.start <= src0.stop < src.stop:  # left intersection
        return range(src.start, src0.stop)
    elif src.start < src0.start <= src.stop <= src0.stop:  # right intersection
        return range(src0.start, src.stop)
    else:
        raise NotImplementedError(f"{src0=}, {src=}")


def r1_inside_r2(r1: range, r2: range):
    return r2.start <= r1.start <= r1.stop <= r2.stop


def intersect(range1: range, range2: range):
    return not (range1.stop < range2.start or range1.start > range2.stop)


def collapse(list_of_ranges: list[range]):
    list_of_ranges.sort(key=lambda x: x.start)
    idx = len(list_of_ranges) - 1
    while idx > 0:
        r1, r2 = list_of_ranges[idx - 1], list_of_ranges[idx]
        if r1.stop == r2.start:
            list_of_ranges[idx - 1] = range(r1.start, r2.stop)
            list_of_ranges.remove(r2)
        idx -= 1
