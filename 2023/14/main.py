import numpy as np
from tools import get_array, print_part


def get_partition_indices(row: np.array) -> list[range]:
    index_max = len(row)
    blocks = [-1] + np.where(row == "#")[0].tolist() + [index_max]
    if len(blocks) > 1:
        return [
            range(blocks[i] + 1, blocks[i + 1])
            for i in range(len(blocks) - 1)
            if (blocks[i] + 1) != blocks[i + 1]
        ]
    else:
        return [range(0, index_max)]


def get_partition(row: np.array, indices: range) -> np.array:
    return row[indices.start : indices.stop]


def roll_rocks_west(terrain: np.array):
    for row in terrain:
        for partition_indices in get_partition_indices(row):
            partition = get_partition(row, partition_indices)
            if num_rocks := np.where(partition == "O")[0].shape[0]:
                partition[0:num_rocks] = "O"
                partition[num_rocks:] = "."


def roll_rocks_east(terrain: np.array):
    for row in terrain:
        for partition_indices in get_partition_indices(row):
            partition = get_partition(row, partition_indices)
            if num_rocks := np.where(partition == "O")[0].shape[0]:
                partition[-num_rocks:] = "O"
                partition[:-num_rocks] = "."


def roll_rocks_north(terrain: np.array):
    roll_rocks_west(terrain.T)


def roll_rocks_south(terrain: np.array):
    roll_rocks_east(terrain.T)


def get_load_north(terrain: np.array):
    return sum(
        [i * sum(row == "O") for i, row in enumerate(reversed(terrain), start=1)]
    )


@print_part
def solve(filepath: str, part: int):
    terrain = get_array(filepath)

    if part == 1:
        roll_rocks_north(terrain)
        load = get_load_north(terrain)
    else:
        states, loads = dict(), dict()
        num_cycles = 1_000_000_000
        cycle_start, period = None, None

        for cycle in range(1, num_cycles + 1):
            roll_rocks_north(terrain)
            roll_rocks_west(terrain)
            roll_rocks_south(terrain)
            roll_rocks_east(terrain)

            state = np.argwhere(terrain == "O").tobytes()
            if state in states.values():
                for c, s in states.items():
                    if s == state:
                        cycle_start = c
                        period = cycle - c
                        break
                break

            states[cycle] = state
            loads[cycle] = get_load_north(terrain)

        corresp_cycle = cycle_start + (num_cycles - cycle_start) % period
        load = loads[corresp_cycle]

    print(load)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
