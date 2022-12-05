from tools import parse_lines, print_part


class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.is_head = False
        self._is_tail = False

    @property
    def coord(self):
        return self.x, self.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def _init_history(self):
        self._history = set()
        self._history.add(self.coord)

    @property
    def is_tail(self) -> bool:
        return self._is_tail

    @is_tail.setter
    def is_tail(self, value: bool):
        if value:
            self._is_tail = value
            self._init_history()

    @property
    def history(self):
        return self._history


def is_connected(p1: Point, p2: Point) -> bool:
    dist_sq = abs(p1.x - p2.x) ** 2 + abs(p1.y - p2.y) ** 2
    is_diagonal_connected = abs(p1.x - p2.x) == 1 and abs(p1.y - p2.y) == 1
    return dist_sq == 1 or dist_sq == 0 or is_diagonal_connected


def is_vertical(p1: Point, p2: Point) -> bool:
    return p1.x == p2.x


def is_horizontal(p1: Point, p2: Point) -> bool:
    return p1.y == p2.y


def move_horz(head: Point, tail: Point, diff: int) -> bool:
    success = True
    if is_horizontal(head, tail):
        tail.x = tail.x + diff
    elif is_vertical(head, tail):
        tail.y = (tail.y + head.y) // 2
    else:
        success = False
    return success


def move_vert(head: Point, tail: Point, diff: int) -> bool:
    success = True
    if is_horizontal(head, tail):
        tail.x = (tail.x + head.x) // 2
    elif is_vertical(head, tail):
        tail.y = tail.y + diff
    else:
        success = False
    return success


def move_diag(head: Point, tail: Point) -> None:
    tail.x = tail.x + (1 if head.x > tail.x else -1)
    tail.y = tail.y + (1 if head.y > tail.y else -1)


def move_points(points: list[Point], direction: str, magnitude: int):
    is_horz_command: bool = direction == "R" or direction == "L"
    is_positive_magnitude: bool = direction == "R" or direction == "U"

    move = move_horz if is_horz_command else move_vert
    diff = 1 if is_positive_magnitude else -1

    for _ in range(magnitude):
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]

            if p1.is_head:
                if is_horz_command:
                    p1.x += diff
                else:
                    p1.y += diff

            if is_connected(p1, p2):
                break
            else:
                move_ok = move(p1, p2, diff)
                if not move_ok:
                    move_diag(p1, p2)
                assert is_connected(p1, p2)

        if p2.is_tail:
            p2.history.add(p2.coord)


@print_part
def solve(filepath: str, part: int = 1):
    commands = [
        (line.split()[0], int(line.split()[1])) for line in parse_lines(filepath)
    ]

    num_points = 2 if part == 1 else 10
    points = [Point() for _ in range(num_points)]

    head, tail = points[0], points[-1]
    head.is_head = True
    tail.is_tail = True

    for command in commands:
        move_points(points, *command)

    print(len(tail.history))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    # FILEPATH = "input_long.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
