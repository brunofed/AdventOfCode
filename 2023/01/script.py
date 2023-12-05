import pandas as pd
from pathlib import Path

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def get_ten_numbers():
    df = pd.DataFrame(
        {"number": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]})
    df["actual_number"] = [str(i) for i in range(1,10)]
    df["first_letter"] = [n[0] for n in df["number"]]
    df["last_letter"] = [n[-1] for n in df["number"]]
    return df

def get_problematic_words(df):
    common_letters = set(df.first_letter).intersection(set(df.last_letter)) # {'o', 'n', 't', 'e'}
    problematic_words = {}
    for row1 in df.itertuples():
        last_lett = row1.last_letter
        if last_lett in common_letters: # e.g. "one"
            for row2 in df.itertuples():
                if row2.first_letter==last_lett: # e.g. "eight"
                    first = row1.number
                    second = row2.number
                    problematic_words[first[:-1] + second] = first + second # "oneight" : "oneeight"
    return problematic_words

def solve(input, df, problematic_words):
    sum = 0
    for word in input:
        new_word = word
        for problem, solution in problematic_words.items(): # address issues of overlapping number names
            new_word = new_word.replace(problem, solution)
        for row in df.itertuples(): # since we are there, also address the issue of having characters
            new_word = new_word.replace(row.number, row.actual_number) # convert number names to numbers
        new_word = new_word.strip(ALPHABET) # remove remaining alphabetic characters
        resulting_number = new_word[0] + new_word[-1] # keep only first and last numbers
        sum += int(resulting_number)
    return sum    

def get_input(this_folder, input_filename):
    with open(Path(this_folder, input_filename + '.txt'), 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

if __name__ == '__main__':
    this_folder = Path(__file__).parent
    df = get_ten_numbers()
    problematic_words = get_problematic_words(df)
    for input_filename in ["input_example", "input"]:
        input = get_input(this_folder, input_filename)
        result = solve(input, df, problematic_words)
        pass