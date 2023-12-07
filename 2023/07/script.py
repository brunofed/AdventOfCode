# import stuff
from os.path import dirname, realpath, join
from csv import reader

# actual math stuff
from collections import Counter
from dataclasses import dataclass


def read(filename, blank_rows=False, rows_with_spaces=False, dir_path=None):
    if dir_path is None:
        dir_path = dirname(realpath(__file__))
    with open(join(dir_path, f"{filename}.txt"), "r") as file:
        if blank_rows:
            grouped_rows = [[]]
            idx = 0
            for row in reader(file):
                if row:
                    grouped_rows[idx].append(row[0])
                else:
                    grouped_rows.append([])
                    idx += 1
            return grouped_rows
        if rows_with_spaces:
            lines = file.readlines()
            return [line.rstrip() for line in lines]
        return [row[0] for row in reader(file)]


@dataclass
class Card:
    value: str

    def ordering(self):
        ALL_CARDS = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        ALL_CARDS.reverse()  # we want lower indices to correspond to lower cards
        return ALL_CARDS.index(self.value)

    def __lt__(self, other):
        return self.ordering() < other.ordering()


@dataclass
class Hand:
    cards: list[Card]

    def __post_init__(self):
        assert len(self.cards) == 5

    @property
    def as_counter(self):
        return Counter(self.cards)

    def top_2_frequencies(self):
        if self.cards == [self.cards[0]] * 5:  # it's a 5 of a kind, so there are no 2 most common types
            return (5, 0)
        most_common, second_most_common = self.as_counter.most_common(2)
        return (most_common[1], second_most_common[1])

    def __lt__(self, other):
        type_self = self.top_2_frequencies()
        type_other = other.top_2_frequencies()
        if type_self != type_other:
            return type_self < type_other
        # they are of the same type, e.g. both four-of-a-kind, so
        # in lexicographic order we compare their cards
        for card_self, card_other in zip(self.cards, other.cards):
            if card_self != card_other:
                return Card(card_self) < Card(card_other)
        return False  # they are the same hand


def parse_input_str(inputs_str):
    hands_bids = []
    for row in inputs_str:
        hand_str, bid_str = row.split()
        hand = list(hand_str)
        bid = int(bid_str)
        hands_bids.append((Hand(hand), bid))
    return hands_bids


def problem1(input):
    hands_bids_sorted = sorted(input, key=lambda x: x[0])
    return sum(rank * bid for rank, (hand, bid) in enumerate(hands_bids_sorted, start=1))


def problem2(input):
    pass


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 6440 if filename == "input_example" else 245794640
        assert problem1(input) == expected_result1
        expected_result2 = None if filename == "input_example" else None
        assert problem2(input) == expected_result2
    pass
