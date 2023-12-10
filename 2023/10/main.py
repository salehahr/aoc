import numpy as np
from tools import parse_lines, print_part

Coordinates = tuple[int, int]


PIPES = "F-7|JL"


get_north = lambda coord: (coord[0] - 1, coord[1])
get_south = lambda coord: (coord[0] + 1, coord[1])
get_west = lambda coord: (coord[0], coord[1] - 1)
get_east = lambda coord: (coord[0], coord[1] + 1)


def get_next_coords(coord: Coordinates, pipe: str) -> tuple[Coordinates, ...]:
    match pipe:
        case "F":
            return get_south(coord), get_east(coord)
        case "-":
            return get_west(coord), get_east(coord)
        case "7":
            return get_west(coord), get_south(coord)
        case "|":
            return get_north(coord), get_south(coord)
        case "J":
            return get_north(coord), get_west(coord)
        case "L":
            return get_north(coord), get_east(coord)


def get_neighbours(
    coord: Coordinates, pipe_map: np.array, history: set[Coordinates]
) -> set[Coordinates]:
    neighbours = set(get_next_coords(coord, pipe_map[coord]))

    for neighbour in list(neighbours):
        if neighbour in history or pipe_map[neighbour] not in PIPES:
            neighbours.remove(neighbour)

    return neighbours


def get_data(filepath: str) -> [np.array, Coordinates]:
    """
    Returns input as a padded array as well as the start coordinates.
    """
    lines = np.array([list(line) for line in parse_lines(filepath)])
    pipe_map = np.pad(lines, pad_width=1, constant_values=".")
    start_rc = tuple(zip(*np.where(pipe_map == "S")))[0]

    # setting of start symbol -- hard coded (!)
    for file_substring, start_symbol in [
        ("short2.txt", "7"),
        ("short.txt", "F"),
        ("input_", "7"),
        ("input.txt", "|"),
    ]:
        if file_substring in filepath:
            pipe_map[start_rc] = start_symbol
            break
    else:
        raise Exception

    return pipe_map, start_rc


def traverse(pipe_map: np.array, init_rc: Coordinates) -> set[Coordinates]:
    """
    Traverses the map and returns a set of the path coordinates.
    """
    history = {init_rc}
    current_rcs = get_neighbours(init_rc, pipe_map, history)

    while current_rcs:
        history |= current_rcs
        current_rcs = {
            n for nrc in current_rcs for n in get_neighbours(nrc, pipe_map, history)
        }

    return history


def get_ordered_history(
    history: set[Coordinates], pipe_map: np.array, init_coord: Coordinates
) -> list[Coordinates]:
    """
    Returns history data in the order of map traversal.
    """
    path_rc = init_coord
    ordered_hist = []
    history_copy = set(list(history))
    while history_copy:
        history_copy.remove(path_rc)
        ordered_hist.append(path_rc)
        if neighbours := get_neighbours(path_rc, pipe_map, ordered_hist):
            path_rc = neighbours.pop()
    return ordered_hist


def get_up_down_map(
    ordered_history: list, pipe_map: np.array, start_rc: Coordinates
) -> np.array:
    """
    Marks
    """
    up_down_map = np.empty(pipe_map.shape, dtype=str)

    pipe0 = pipe_map[start_rc]
    direction = "d"

    up_down_map[start_rc] = direction
    pipe_map[start_rc] = "X"

    for rc in ordered_history[1:]:
        pipe = pipe_map[rc]
        if pipe0 + pipe in ["LJ", "F7", "JL", "7F"]:  # U-turn
            direction = "u" if direction == "d" else "d"
        if pipe == "-":
            up_down_map[rc] = "-"
        else:
            up_down_map[rc] = direction
            pipe0 = pipe

        pipe_map[rc] = "X"

    return up_down_map


def count_tiles(up_down_map: np.array, pipe_map: np.array) -> [int, int]:
    tiles_between_ud, tiles_between_du = 0, 0

    for r, c in np.argwhere(pipe_map != "X"):  # not path
        if left_dir := [x for x in up_down_map[r, :c] if x in ["d", "u"]]:
            left_dir = left_dir[-1]
        else:
            continue

        if right_dir := [x for x in up_down_map[r, c:] if x in ["d", "u"]]:
            right_dir = right_dir[0]
        else:
            continue

        if left_dir + right_dir == "ud":
            tiles_between_ud += 1
        elif left_dir + right_dir == "du":
            tiles_between_du += 1

    return tiles_between_ud, tiles_between_du


@print_part
def solve(filepath: str, part: int):
    pipe_map, start_rc = get_data(filepath)
    history = traverse(pipe_map, start_rc)

    if part == 1:
        distance = len(history) // 2
        print(distance)
    else:
        ordered_hist = get_ordered_history(history, pipe_map, start_rc)
        up_down_map = get_up_down_map(ordered_hist, pipe_map, start_rc)
        tiles_between_ud, tiles_between_du = count_tiles(up_down_map, pipe_map)
        print(f"{tiles_between_ud=}, {tiles_between_du=}")


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
