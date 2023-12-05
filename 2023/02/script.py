from math import prod
from pathlib import Path
import pandas as pd


COLOURS = ['red', 'green', 'blue']

def problem1(games):
    constraints = {'red': 12, 'green': 13, 'blue': 14}
    sum = 0
    for i, game in enumerate(games, start=1):
        if game.apply(lambda row: all(row[k] <= v for k, v in constraints.items()), axis=1).all():
           sum += i 
    return sum

def problem2(games):
    return sum(prod(game.max()) for game in games)

def get_input(this_folder, input_filename):
    with open(Path(this_folder, input_filename + '.txt'), 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def process_input(raw_input):
    games = []
    for line in raw_input:
        game_list = []
        game = line.split(': ')[1]
        rounds = game.split('; ')
        for round in rounds:
            balls = round.split(', ')
            balls_dict = {colour: 0 for colour in COLOURS}
            for num_colour in balls:
                num, colour = num_colour.split()
                balls_dict[colour] = int(num)
            game_list.append(balls_dict)
        df = pd.DataFrame(game_list, columns=COLOURS)
        games.append(df)
    return games

if __name__ == '__main__':
    this_folder = Path(__file__).parent

    for input_filename in ["input_example", "input"]:
        raw_input = get_input(this_folder, input_filename)
        input = process_input(raw_input)
        result1 = problem1(input)
        result2 = problem2(input)
        pass