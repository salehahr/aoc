import re

from tools import parse_lines, print_ans, print_part


def traverse(from_, to_, been_to: list, locations, total_dist, next_dist, prev_d=0):
    path = been_to + [to_]
    total_dist[tuple(path)] = prev_d + next_dist[from_, to_]
    for next_ in locations - set(path):
        traverse(
            to_,
            next_,
            path,
            locations,
            total_dist,
            next_dist,
            total_dist[tuple(path)],
        )


@print_part
def solve(filepath: str, part: int = 1):
    D = dict()
    for line in parse_lines(filepath):
        s, e, d = re.match(r"(\w+) to (\w+) = (\d+)", line).groups()
        D[s, e] = int(d)
        D[e, s] = int(d)
    locations = list(set([loc for start_end in D.keys() for loc in start_end]))

    pd = dict()
    for start_, to_ in [(s, t) for s in locations for t in set(locations) - {s}]:
        traverse(start_, to_, [start_], set(locations), pd, D)

    operator = min if part == 1 else max
    print_ans(
        operator([d for p, d in pd.items() if len(p) == len(locations)]),
        251 if part == 1 else 898,
    )


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
