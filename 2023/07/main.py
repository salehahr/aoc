from collections import defaultdict
from functools import cmp_to_key

from HandType import HandType
from tools import parse_lines, print_part

CARD_RANK_p1 = list(reversed("AKQJT98765432"))
CARD_RANK_p2 = list(reversed("AKQT98765432J"))


def get_hand_type(hand: str, use_wildcard: bool) -> HandType:
    unique_cards = list(set(hand))
    num_unique_cards = len(unique_cards)

    if use_wildcard:
        match num_unique_cards:
            case 1 | 2:  # [5], [1, 4], [2, 3]
                return HandType.FIVE_KIND
            case 3:  # [3, 1, 1] [2, 2, 1]
                if 3 in [hand.count(x) for x in unique_cards] or hand.count("J") == 2:
                    return HandType.FOUR_KIND
                else:
                    return HandType.FULL_HOUSE
            case 4:
                return HandType.THREE_KIND
            case 5:
                return HandType.ONE_PAIR

    match num_unique_cards:
        case 1:  # [5]
            return HandType.FIVE_KIND
        case 2:  # [1, 4] [2, 3]
            if 4 in [hand.count(x) for x in unique_cards]:
                return HandType.FOUR_KIND
            else:
                return HandType.FULL_HOUSE
        case 3:  # [3, 1, 1] [2, 2, 1]
            if 3 in [hand.count(x) for x in unique_cards]:
                return HandType.THREE_KIND
            else:
                return HandType.TWO_PAIR
        case 4:  # [2, 1, 1, 1]
            return HandType.ONE_PAIR
        case 5:
            return HandType.HIGH


def compare_two_hands(part: int):
    card_rank = eval(f"CARD_RANK_p{part}")

    def __comparer(*hand_bids: tuple[str, int]):
        hands, _ = zip(*hand_bids)
        for h1_card, h2_card in zip(*hands):
            c1_rank, c2_rank = card_rank.index(h1_card), card_rank.index(h2_card)
            if c1_rank == c2_rank:
                continue
            return -1 if c1_rank < c2_rank else 1
        else:
            return 0

    return cmp_to_key(__comparer)


def sorted_bids(hand_bids: list[tuple[str, int]], part: int) -> list[tuple[str, int]]:
    data = defaultdict(list, {k: [] for k in HandType})
    hand_ranks = compare_two_hands(part)

    for hand, bid in hand_bids:
        hand_type = get_hand_type(hand, use_wildcard=(part == 2 and "J" in hand))
        data[hand_type].append((hand, bid))
        data[hand_type] = sorted(data[hand_type], key=hand_ranks)

    return [bid for hand_bids in reversed(data.values()) for hand, bid in hand_bids]


def get_hand_bid(line: str) -> tuple[str, int]:
    hand, num = line.split()
    return hand, int(num)


@print_part
def solve(filepath: str, part: int = 1):
    hand_bids = [get_hand_bid(line) for line in parse_lines(filepath)]
    data = sorted_bids(hand_bids, part)
    wins = sum([i * bid for i, bid in enumerate(data, start=1)])
    print(wins)


if __name__ == "__main__":
    # FILEPATH = "input_short.txt"
    FILEPATH = "input.txt"

    solve(FILEPATH, part=1)
    solve(FILEPATH, part=2)
