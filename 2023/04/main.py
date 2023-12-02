import re

from tools import parse_lines, print_part

WINNING_NUMBERS_PATTERN = r"\d+\s+"
NUMBERS_IN_HAND_PATTERN = r"\d+\s*"


@print_part
def solve(filepath: str, part: int = 1):
    cards = [line.split(r"|") for line in parse_lines(filepath)]

    points = 0
    num_cards = [1] * len(cards)

    for card, (wins, haves) in enumerate(cards):
        win_nums = set(w.strip() for w in re.findall(WINNING_NUMBERS_PATTERN, wins))
        have_nums = set(w.strip() for w in re.findall(NUMBERS_IN_HAND_PATTERN, haves))
        num_matches = len(have_nums & win_nums)

        if part == 1:
            power = num_matches - 1
            points += (2**power) if power >= 0 else 0
        else:
            next_cards = list(range(card + 1, card + 1 + num_matches))
            for card_idx in next_cards:
                num_cards[card_idx] += num_cards[card]

    if part == 1:
        print(points)
    else:
        print(sum(num_cards))


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
