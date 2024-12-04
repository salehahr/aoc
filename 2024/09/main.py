import itertools

from tools import parse_lines, print_ans, print_part


@print_part
def solve(filepath: str, part: int = 1):
    disk_map = parse_lines(filepath).pop()
    files, spaces = list(map(int, disk_map[0::2])), map(int, disk_map[1::2])
    total_blocks = sum(files)

    # replace integers with characters to only take up one space per block
    space_char = chr(len(files))
    file_str = (chr(i) * x for i, x in enumerate(files))
    space_str = (space_char * x for i, x in enumerate(spaces))
    layout = "".join(
        xx for x in itertools.zip_longest(file_str, space_str) for xx in x if xx
    )

    l1, l2 = layout[:total_blocks], layout[total_blocks:]
    l2 = [x for x in l2 if x != space_char]
    l2.reverse()
    num_spaces_to_remove = l1.count(space_char)
    assert num_spaces_to_remove == len(l2), f"{num_spaces_to_remove=} != {len(l2)=}"

    non_space_idxs = (i for i, x in enumerate(l1) if x != space_char)
    space_idxs = (i for i, x in enumerate(l1) if x == space_char)

    sum_non_space = sum(i * ord(l1[i]) for i in non_space_idxs)
    sum_space = sum(i * ord(n) for i, n in zip(space_idxs, l2))
    ans = sum_space + sum_non_space

    if part == 1:
        print_ans(ans, correct_ans=6446899523367)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    # solve(FILEPATH, part=2)
