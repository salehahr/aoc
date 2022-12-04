# https://adventofcode.com/2021/day/6
import context

from tools import parse_lines, print_part

State = list[int]


def initialise(init_state: State) -> State:
    NUM_STATES = 9
    state = [0] * NUM_STATES
    for num in init_state:
        state[num] = state[num] + 1
    return state


def update_state(state: State):
    respawned = state[0]
    state[:] = state[1:] + [0]
    state[6] = state[6] + respawned
    state[8] = respawned


@print_part
def solve(filepath: str, part: int = 1):
    init_state = [int(x) for x in parse_lines(filepath)[0].split(",")]
    state = initialise(init_state)

    num_days = 80 if part == 1 else 256
    for day in range(1, num_days + 1):
        update_state(state)

    print(sum(state))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
