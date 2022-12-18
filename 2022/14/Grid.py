import numpy as np

AIR = "."
ROCK = "#"
SAND = "o"


def get_limits(rock_paths, part):
    all_x, all_y = zip(*[(x, y) for path in rock_paths for x, y in path])
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    min_y = 0
    if part == 2:
        max_y += 2
        width = max_x - min_x + 1
        min_x -= width
        max_x += 2 * width
    return min_x, max_x, min_y, max_y


class Grid:
    def __init__(self, rock_paths, part):
        minx, maxx, miny, maxy = get_limits(rock_paths, part)
        self._min_x = minx
        self._max_y = maxy

        height = maxy - miny + 1
        self.height = height
        self.width = maxx - minx + 1 if part == 1 else height * 3

        self.array = np.full((height, self.width), AIR)
        self._sand_rc = None

        self._prev_path = []

        self._init_rocks(rock_paths, part)

    def _init_rocks(self, rock_paths, part):
        for path in rock_paths:
            for i in range(len(path) - 1):
                xy1, xy2 = path[i], path[i + 1]
                self._draw_path(xy1, xy2)

        if part == 2:
            self.array[-1, :] = ROCK

    def _draw_path(self, xy1, xy2):
        r1, c1 = self._convert_rc(*reversed(xy1))
        r2, c2 = self._convert_rc(*reversed(xy2))

        r1, r2 = (r1, r2) if r1 <= r2 else (r2, r1)
        c1, c2 = (c1, c2) if c1 <= c2 else (c2, c1)

        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                self.array[r, c] = ROCK

    def start(self, part):
        no_more = False
        count = 0 if part == 1 else 1
        while not no_more:
            count += 1

            if self._prev_path:
                self._draw_sand(self._prev_path[-1])
            else:
                self._draw_sand()

            no_more = getattr(self, f"_move_sand_p{part}")()
        print(count - 1)

    def _move_sand_p1(self):
        at_rest = False
        no_more = False

        while not (at_rest or no_more):
            for delta in [[1, 0], [1, -1], [1, 1]]:
                r, c = np.array(self._sand_rc) + delta
                if 0 <= r < self.height and 0 <= c < self.width:
                    if self._is_free(r, c):
                        self._prev_path.append((r, c))
                        self.array[*self._sand_rc] = AIR
                        self._draw_sand((r, c))
                        break
                else:
                    no_more = True
                    break
            else:
                self._prev_path.pop()
                self._sand_rc = None
                at_rest = True
        return no_more

    def _move_sand_p2(self):
        at_rest = False
        no_more = False

        while not (at_rest or no_more):
            deltas = [[1, 0], [1, -1], [1, 1]]
            rcs = [np.array(self._sand_rc) + delta for delta in deltas]

            if self._sand_rc == self._convert_rc(0, 500) and not any(
                self._is_free(*rc) for rc in rcs
            ):
                no_more = True
                break

            for delta in deltas:
                r, c = np.array(self._sand_rc) + delta
                if self._is_free(r, c):
                    self._prev_path.append((r, c))
                    self.array[*self._sand_rc] = AIR
                    self._draw_sand((r, c))
                    break
            else:
                self._prev_path.pop()
                self._sand_rc = None
                at_rest = True
        return no_more

    def _draw_sand(self, rc=None):
        if rc is None:
            if self._sand_rc is None:
                self._sand_rc = self._convert_rc(0, 500)
        else:
            self._sand_rc = rc
        self.array[*self._sand_rc] = SAND

    def _convert_rc(self, r, c):
        return r, c - self._min_x

    def _is_free(self, r, c):
        return self.array[r, c] == AIR

    def print(self):
        print(self.array)
