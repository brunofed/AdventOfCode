# import stuff
from os.path import dirname, realpath, join
from csv import reader

# actual math stuff
from collections import Counter
from dataclasses import dataclass
from typing import NamedTuple

J = "J"


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


def replace(l: list, old_value, new_value):
    return [new_value if x == old_value else x for x in l]


@dataclass
class Card:
    value: str
    _problem_num: int

    def ordering(self):
        ALL_CARDS = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]  # actually, there is no J
        if self._problem_num == 1:
            ALL_CARDS.insert(3, J)
        else:
            ALL_CARDS.append(J)
        # so the 2 orderings are
        # 1) ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        # 2) ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
        ALL_CARDS.reverse()  # we want lower indices to correspond to lower cards
        return ALL_CARDS.index(self.value)

    def __lt__(self, other):
        return self.ordering() < other.ordering()


@dataclass
class Hand:
    cards: list[str]
    _problem_num: int
    virtual_hand: None

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

    def change_jacks(self):
        new_possible_hands = []
        for card_type in set(self.cards) - {J}:
            new_hand = Hand(replace(self.cards, J, card_type), self._problem_num)
            new_possible_hands.append(new_hand)
        self.virtual_hand = max(new_possible_hands).cards

    def __lt__(self, other):
        type_self = self.top_2_frequencies()
        type_other = other.top_2_frequencies()
        if type_self != type_other:
            if self._problem_num == 2:
                if J in self.cards:
                    self.change_jacks()
                if J in other.cards:
                    other.change_jacks()
                # update hand type
                type_self = self.top_2_frequencies()
                type_other = other.top_2_frequencies()
            return type_self < type_other
        # they are of the same type, e.g. both four-of-a-kind, so
        # in lexicographic order we compare their cards
        for card_self, card_other in zip(self.cards, other.cards):
            if card_self != card_other:
                return Card(card_self, self._problem_num) < Card(card_other, self._problem_num)
        return False  # they are the same hand


def parse_input_str(inputs_str):
    players = []
    for row in inputs_str:
        hand_str, bid_str = row.split()
        hand = list(hand_str)
        bid = int(bid_str)
        players.append((hand, bid))
    return players


class Player(NamedTuple):
    hand: Hand
    bid: int


def problem(input, problem_num):
    players = [Player(Hand(hand, problem_num), bid) for hand, bid in input]
    players_sorted = sorted(players, key=lambda player: player.hand)
    return sum(rank * player.bid for rank, player in enumerate(players_sorted, start=1))


if __name__ == "__main__":
    for filename in ["input_example", "input"]:
        inputs_str = read(filename)
        input = parse_input_str(inputs_str)

        expected_result1 = 6440 if filename == "input_example" else 245794640

        assert problem(input, 1) == expected_result1
        expected_result2 = 5905 if filename == "input_example" else None
        assert problem(input, 2) == expected_result2
    pass
