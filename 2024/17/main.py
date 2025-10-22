import sys

from tools import parse_lines, print_ans, print_part


def _get_b(a: int) -> int:
    amod8xor5 = (a % 8) ^ 5
    return (a >> amod8xor5) % 8 ^ amod8xor5 ^ 6


@print_part
def solve(filepath: str, part: int = 1):
    *registers, program = tuple(line for line in parse_lines(filepath) if line)

    if part == 1:
        registers_str = (l.replace("Register ", "").split(": ") for l in registers)
        registers: dict[str, int] = {k: int(v) for k, v in registers_str}
        aval, output = registers["A"], []

        while aval:
            bval = _get_b(aval)
            output.append(bval)
            aval >>= 3
        output = ",".join(map(str, output))
    else:
        program = tuple(int(x) for x in program.split(": ")[-1].split(","))
        a0 = sys.maxsize
        tries = [(len(program), program[-1])]

        while tries:
            i_next, a_next = tries.pop()
            i = i_next - 1
            a_min = int(oct(a_next) + "0", 8)
            a_max = int(oct(a_next) + "7", 8)

            # try to find a_i
            for a_i in range(a_min, a_max + 1):
                div_ok = (a_i >> 3) == a_next
                b_ok = _get_b(a_i) == program[i]
                if div_ok and b_ok:
                    if i == 0:
                        a0 = min(a_i, a0)
                    else:
                        tries.append((i, a_i))
        output = a0

    print_ans(output, correct_ans="2,1,3,0,5,2,3,7,1" if part == 1 else 107416732707226)


if __name__ == "__main__":
    # FILEPATH = "input_short"
    FILEPATH = "input"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
