# https://adventofcode.com/2021/day/8
from collections import Counter
from typing import Optional

import context

from tools import parse_lines, print_part

Signal = str
Signals = list[Optional[Signal]]
EventSignals = list[Signals]

ORIG_DIGIT_MAP = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}
REVERSED_DIGIT_MAP = {v: k for k, v in ORIG_DIGIT_MAP.items()}
char_map = {chr(x): None for x in list(range(ord("a"), ord("g") + 1))}

NUM2LENGTH_MAP = {
    k: len(v) for k, v in sorted(ORIG_DIGIT_MAP.items(), key=lambda item: len(item[1]))
}


def parse_obsservations_and_output(filepath: str) -> tuple[EventSignals, EventSignals]:
    inp_out: list[list[str]] = [line.split(" | ") for line in parse_lines(filepath)]
    observations, outputs = [list(x) for x in zip(*inp_out)]

    parse_signals(observations, sort=True)
    parse_signals(outputs, sort=False)

    return observations, outputs


def parse_signals(event_signals: list[str], sort: bool):
    """
    Modifies type of event_signals from list[str] to EventSignals == list[list[Signal]].
    An event contains a list of signals.
    Each entry (list of segments) in the list of signals is modified so that
        the segments are in alphabetical order.
    The list of entries can optionally be sorted by length.
    """
    for i, signals_str in enumerate(event_signals):
        signals: Signals = signals_str.split()

        # sort each entry
        sort_entries(signals)

        # sort list by entry length
        if sort:
            signals.sort(key=lambda x: len(x))

        event_signals[i]: Signals = signals


def sort_entries(signals: Signals | list[list[str]]):
    """Sorts each single entry in the list of signals."""
    for i, signal in enumerate(signals):
        signal: Signal = sort_entry(signal)
        signals[i]: Signal = signal


def sort_entry(signal: Signal) -> Signal:
    """Sorts signal in alphabetical order."""
    signal: list[chr] = [*signal]
    signal.sort()
    return "".join(signal)


def length2signal(signals: Signals) -> dict[int, set]:
    LENGTH_VALUES = list(NUM2LENGTH_MAP.values())
    l2s = {
        length: set([signal for signal in signals if len(signal) == length])
        for length in LENGTH_VALUES
    }
    return {k: [set(av) for av in v] for k, v in l2s.items()}


def solve_char_map(inputs):
    l2smap = length2signal(inputs)

    options_cf = l2smap[2][0]
    options_acf = l2smap[3][0]
    options_bcdf = l2smap[4][0]
    options_abcdefg = l2smap[7][0]

    char_map["a"] = (options_acf - options_cf).pop()

    options_bd = options_bcdf - options_cf
    options_bdeg = options_abcdefg - options_acf
    options_eg = options_bdeg - options_bd

    if len(l5s := l2smap[5]) == 3:
        options_acdfg = [signal for signal in l5s if options_cf.issubset(signal)][0]
        options_be = options_abcdefg - options_acdfg

        char_map["b"] = options_bd.intersection(options_be).pop()
        char_map["e"] = options_be.difference(get_char_map("b")).pop()
        char_map["d"] = options_bd.difference(get_char_map("b")).pop()
        char_map["g"] = options_eg.difference(get_char_map("e")).pop()

        options_acdge = [signal for signal in l5s if get_char_map("e").issubset(signal)][0]
        char_map["c"] = (options_cf & options_acdge).pop()
        char_map["f"] = options_cf.difference(get_char_map("c")).pop()


def get_char_map(key: str) -> set:
    return set(char_map[key])


def concat_output(output_signals: Signals) -> Signals | int:
    assert all([isinstance(x, int) for x in output_signals])
    return int("".join([str(x) for x in output_signals]))


@print_part
def solve(filepath: str, part: int = 1):
    observations, outputs = parse_obsservations_and_output(filepath)

    if part == 1:
        length_values: list[int] = list({
            k: v for k, v in NUM2LENGTH_MAP.items() if k in [1, 4, 7, 8]
        }.values())
        n_1478 = 0
        for output in outputs:
            n_1478 += len([x for x in output if len(x) in length_values])
        print(n_1478)
    else:
        sum_output = 0

        for inp, outp in zip(observations, outputs):
            solve_char_map(inp)
            reversed_char_map = {v: k for k, v in char_map.items()}

            parsed_outputs: list[list[str]] = [[reversed_char_map[n] for n in x] for x in outp]
            sort_entries(parsed_outputs)

            for i, parsed_e in enumerate(parsed_outputs):
                outp[i] = REVERSED_DIGIT_MAP[parsed_e]
            sum_output += concat_output(outp)

        print(sum_output)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
