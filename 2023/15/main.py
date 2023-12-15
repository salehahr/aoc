import re
from collections import defaultdict

from tools import parse_lines, print_part


def get_hash_char(input_char: str, start_hash: int = 0):
    hash_val = start_hash
    hash_val = ((hash_val + ord(input_char)) * 17) % 256
    return hash_val


def get_hash(input_string: str):
    hash_val = 0
    for c in input_string:
        hash_val = get_hash_char(c, start_hash=hash_val)
    return hash_val


@print_part
def solve(filepath: str, part: int):
    lines = parse_lines(filepath)[0].split(",")

    if part == 1:
        result = sum([get_hash(line) for line in lines])
        print(result)
    else:
        boxes = defaultdict(dict)
        for i, line in enumerate(lines):
            label, focal_length = re.findall(r"(\w+).?(\d?)", line)[0]
            focal_length = int(focal_length) if focal_length else None
            box = boxes[get_hash(label)]
            if focal_length:
                box[label] = focal_length
            else:
                box.pop(label, None)

        result = 0
        for box_num, lenses in boxes.items():
            for slot, (lens, focal_length) in enumerate(lenses.items(), start=1):
                result += (box_num + 1) * slot * focal_length
        print(result)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
