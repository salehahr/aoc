import re
from itertools import accumulate

from tools import parse_lines, print_part

CD_PATTERN = r"\$ cd (.*)"
FILE_PATTERN = r"(\d+) .*"


@print_part
def solve(filepath: str, part: int = 1):
    cwd, dir_sizes = [], dict()

    for line in parse_lines(filepath):
        if cd_match := re.match(CD_PATTERN, line):
            dir_name = cd_match.group(1)
            if dir_name == "..":
                cwd.pop()
            else:
                dir_name += "" if dir_name == "/" else "/"
                cwd.append(dir_name)

        if file_match := re.match(FILE_PATTERN, line):
            filesize = int(file_match.group(1))

            for cwd_name in accumulate(cwd):
                if cwd_name in dir_sizes:
                    dir_sizes[cwd_name] += filesize
                else:
                    dir_sizes[cwd_name] = filesize

    if part == 1:
        MAX_SIZE = 100000
        total_sizes = sum(
            [size for dir_name, size in dir_sizes.items() if size <= MAX_SIZE]
        )
        print(total_sizes)
    else:
        CAPACITY, SIZE_NEEDED = 70000000, 30000000
        currently_free = CAPACITY - dir_sizes["/"]
        difference_needed = SIZE_NEEDED - currently_free
        min_size = min(
            [size for size in dir_sizes.values() if size > difference_needed]
        )
        print(min_size)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
