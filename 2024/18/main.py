from tools import parse_lines, print_ans, print_part
from tools.generic_types import Coordinates, get_neighbours
from tools.pathfinding import bfs


@print_part
def solve(filepath: str, part: int = 1):
    max_len = 6 if "short" in filepath else 70
    max_len += 1

    start = Coordinates(0, 0)
    end = Coordinates(max_len - 1, max_len - 1)

    bytes_list = [Coordinates(*map(int, l.split(","))) for l in parse_lines(filepath)]

    if part == 1:
        first_kilobyte = bytes_list[:1024]

        def __neighbours(rc: Coordinates) -> set[Coordinates]:
            nbs = get_neighbours(rc, h=max_len, w=max_len)
            return set(nbs) - set(first_kilobyte)

        path = bfs(start_rc=start, end_rc=end, next_states=__neighbours)
        ans = len(path) - 1
    else:
        path, bad_byte = None, None
        while not path:
            bad_byte = bytes_list.pop()

            def __neighbours(rc: Coordinates) -> set[Coordinates]:
                nbs = get_neighbours(rc, h=max_len, w=max_len)
                return set(nbs) - set(bytes_list)

            path = bfs(start_rc=end, end_rc=start, next_states=__neighbours)
        ans = bad_byte
    print_ans(ans, correct_ans=290 if part == 1 else (64, 54))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
