import collections
import re

test_cards = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
scratch_cards = collections.Counter()


def get_match_points(card):
    m = re.match(r'Card\s+[0-9]+: (.*)\|(.*)', card)
    if m:
        winning = {int(n) for n in m.group(1).strip().split(' ') if n}
        scratched = {int(n) for n in m.group(2).strip().split(' ') if n}
        winning_numbers = winning.intersection(scratched)
        if winning_numbers:
            return 2 ** (len(winning_numbers) - 1)
    return 0


def get_total_scratchcards(cards, loop_range=None):
    if loop_range is None:
        loop_range = range(0, len(cards))
    for idx in loop_range:
        card = cards[idx]
        m = re.match(r'Card\s+([0-9]+): (.*)\|(.*)', card)
        if m:
            card_num = int(m.group(1))
            winning = {int(n) for n in m.group(2).strip().split(' ') if n}
            scratched = {int(n) for n in m.group(3).strip().split(' ') if n}
            winning_numbers = winning.intersection(scratched)

            scratch_cards[card_num] += 1
            if winning_numbers:
                copies_range = range(card_num, card_num + len(winning_numbers))
                get_total_scratchcards(cards, copies_range)


if __name__ == '__main__':
    with open('input/04.txt') as f:
        get_total_scratchcards(f.read().splitlines())
        print(scratch_cards.total())
