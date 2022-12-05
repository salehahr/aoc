import numpy as np

from tools import parse_lines, print_part


@print_part
def solve(filepath: str, part: int = 1):
    forest = np.array([[int(c) for c in line] for line in parse_lines(filepath)])
    HEIGHT, WIDTH = forest.shape

    NUM_VISIBLE_EDGES = HEIGHT * 2 + WIDTH * 2 - 4
    num_visible_interior = 0
    max_scenic_score = 0

    for r in range(1, HEIGHT - 1):
        for c in range(1, WIDTH - 1):
            tree = forest[r, c]

            above = np.flip(forest[:r, c])
            below = forest[r + 1 :, c]
            left = np.flip(forest[r, :c])
            right = forest[r, c + 1 :]

            if part == 1:
                horz_visible = all(tree > left) or all(tree > right)
                vert_visible = all(tree > above) or all(tree > below)
                num_visible_interior += horz_visible or vert_visible
            else:
                tree_score = 1

                for dir_array in [above, below, left, right]:
                    dir_score = 0
                    for other_tree in dir_array:
                        if tree <= other_tree:
                            dir_score += 1
                            break
                        elif tree > other_tree:
                            dir_score += 1
                    tree_score *= dir_score

                    if tree_score == 0:
                        break

                max_scenic_score = max(max_scenic_score, tree_score)

    if part == 1:
        print(num_visible_interior + NUM_VISIBLE_EDGES)
    else:
        print(max_scenic_score)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
