import itertools
from collections import namedtuple
from dataclasses import dataclass
from typing import ClassVar

from tools import parse_lines, print_ans, print_part

File = namedtuple("File", field_names=["id", "size"])


@dataclass
class Space:
    CHAR: ClassVar[str] = ""

    files: list[File] = None
    size: int = 0

    def __post_init__(self):
        if not self.files:
            self.files = []

    def __repr__(self) -> str:
        return "".join(chr(f.id) * f.size for f in self.files) + self.CHAR * self.size


def get_layout(files: list[File], spaces: list[Space]) -> str:
    # replace integers with characters to only take up one space per block
    file_str = (f if isinstance(f, str) else chr(f.id) * f.size for f in files)
    space_str = (str(sp) for sp in spaces)

    return "".join(
        xx for x in itertools.zip_longest(file_str, space_str) for xx in x if xx
    )


@print_part
def solve(filepath: str, part: int = 1):
    disk_map = parse_lines(filepath).pop()
    files, spaces = list(map(int, disk_map[0::2])), list(map(int, disk_map[1::2]))
    Space.CHAR = chr(len(files))

    files = [File(id_, size) for id_, size in enumerate(files)]
    spaces = [Space(size=x) for x in spaces]

    if part == 1:
        layout = get_layout(files, spaces)

        total_blocks = sum(f.size for f in files)
        front_part, end_part = layout[:total_blocks], layout[total_blocks:]
        reversed_end_part = list(reversed([x for x in end_part if x != Space.CHAR]))
        assert front_part.count(Space.CHAR) == len(reversed_end_part)

        file_indices = (i for i, x in enumerate(front_part) if x != Space.CHAR)
        space_indices = (i for i, x in enumerate(front_part) if x == Space.CHAR)

        sum_fwd = sum(i * ord(front_part[i]) for i in file_indices)
        sum_bwd = sum(i * ord(n) for i, n in zip(space_indices, reversed_end_part))

        ans = sum_fwd + sum_bwd
    else:
        for file in reversed(files):
            for i, space in enumerate(spaces[: file.id]):
                if space.size >= file.size:
                    # fill space in new location
                    space.files.append(file)
                    space.size -= file.size

                    # replace file with space in orig. location
                    files[file.id] = Space.CHAR * file.size
                    break

        layout = get_layout(files, spaces)

        ans = sum(i * ord(file) for i, file in enumerate(layout) if file != Space.CHAR)

    print_ans(ans, correct_ans=6446899523367 if part == 1 else 6478232739671)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
