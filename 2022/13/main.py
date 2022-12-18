from tools import parse_lines, print_part


def compare_packets(left_packet: list, right_packet: list) -> None | bool:
    """
    Returns True if left_packet is smaller, False otherwise, or None if both
    packets are equal.
    """
    # if only one packet is empty
    if (not left_packet) ^ (not right_packet):
        return not left_packet

    ok = None
    for i, (ll, rr) in enumerate(zip(left_packet, right_packet)):
        if isinstance(ll, int) and isinstance(rr, int):
            if ll == rr:
                ok = unequal_size_list_check(left_packet, right_packet, i)
            else:
                ok = ll < rr

        elif isinstance(ll, list) and isinstance(rr, list):
            if len(ll) == 0 and len(rr) == 0:
                ok = unequal_size_list_check(left_packet, right_packet, i)
            elif len(ll) == 0 or len(rr) == 0:
                ok = len(ll) == 0
            else:
                ok = compare_packets(ll, rr)
                ok = unequal_size_list_check(left_packet, right_packet, i) if ok is None else ok

        else:
            ok = compare_packets([ll], rr) if isinstance(ll, int) else compare_packets(ll, [rr])
            ok = unequal_size_list_check(left_packet, right_packet, i) if ok is None else ok

        if ok is None:
            continue
        else:
            break

    return ok


def unequal_size_list_check(left: list, right: list, idx: int) -> None | bool:
    """
    Returns 'in order' value depending on which list runs out first.
    If neither run out, None is returned.
    """
    if len(left) != len(right):
        if len(left) == idx + 1 or len(right) == idx + 1:
            return len(left) == idx + 1
    return None


@print_part
def solve(filepath: str, part: int = 1):
    lines = [eval(line) if line else None for line in parse_lines(filepath) if not line.startswith("#")]
    n_lines = len(lines)

    if part == 1:
        ok = []
        for i in range(0, n_lines, 3):
            pair_idx = i // 3 + 1
            left_packet, right_packet = lines[i], lines[i+1]
            assert (is_ok := compare_packets(left_packet, right_packet)) is not None
            if is_ok:
                ok.append(pair_idx)
        print(sum(ok))
    else:
        from functools import cmp_to_key

        def compare(p1, p2):
            p1_smaller = compare_packets(p1, p2)
            return -1 if p1_smaller else 1

        lines = [line for line in lines if line is not None]
        lines.append([[2]])
        lines.append([[6]])
        lines.sort(key=cmp_to_key(compare))

        signal1 = lines.index([[2]]) + 1
        signal2 = lines.index([[6]]) + 1
        print(signal1 * signal2)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"
    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
