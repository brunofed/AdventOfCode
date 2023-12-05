import os
from csv import reader
import numpy as np
from collections import Counter
from scipy.sparse import csr_matrix

def get_dir():
    return os.path.dirname(os.path.realpath(__file__))

def read(filename, dir_path):
    with open(os.path.join(dir_path, f'{filename}.txt'), 'r') as file:
        return [row[0] for row in reader(file)]

def insertion_rules_to_dict(insertion_rules):
    rules_dict = {}
    for rule in insertion_rules:
        rule_split =  rule.split(' -> ')
        rules_dict[rule_split[0]] = rule_split[0][0] + rule_split[1] #e.g. if the rule is VS -> B then rules_dict[VS] = VB
    return rules_dict

def insert_position(position, list1, list2):
    return list1[:position] + list2 + list1[position:]

def apply_rules_to_polymer(text, rules_dict):
    new_text = ''
    text_split = get_letters_pairs(text, False)
    for xx in text_split:
        try:
            yy = rules_dict[xx]
        except(KeyError):
            yy = xx
        finally:
            new_text = new_text + yy
    return new_text

def most_and_least_common_letters(text_or_dict):
    counted_text = Counter(text_or_dict).most_common()
    counted_text_nonzero = [x for x in counted_text if x[1]>0]
    return counted_text_nonzero[0], counted_text_nonzero[-1]

def diff_of_most_minus_least_common(text_or_dict):
    most, least = most_and_least_common_letters(text_or_dict)
    return most[1] - least[1]

def problem1(template, insertion_rules, num_steps):
    rules_dict = insertion_rules_to_dict(insertion_rules)
    polymer = template
    for step in range(num_steps):
        polymer = apply_rules_to_polymer(polymer, rules_dict)
    return diff_of_most_minus_least_common(polymer)

def get_letters_pairs_str(text, discard_isolated_last_letter=True):
    # the last text[i:i+2] is the penultimate-ultimate letter if shift = 1, else it's last letter only.
    # If the text has an even number of letters (so after splitting in pairs the last letter is alone), it ignores the last letter
    shift = 1 if discard_isolated_last_letter else 0
    return [text[i:i+2] for i in range(len(text)-shift)]

def get_letters_pairs_dict(explicit_rules_dict):
    pairs = []
    for xy, xz_and_zy in explicit_rules_dict.items():
        pairs += [xy] + xz_and_zy
    return pairs

def two_pairs_from_dict(rules_dict):
    explicit_dict = {}
    for xy, xz in rules_dict.items():
        zy = xz[1] + xy[1] # i.e. if rules_dict[AB] = AC then y2x2 = CB
        explicit_dict[xy] = [xz, zy]
    return explicit_dict

def get_letters_pairs(template, explicit_rules_dict):
    all_letters_pairs = get_letters_pairs_str(template) + get_letters_pairs_dict(explicit_rules_dict)
    return list(set(all_letters_pairs))

def create_initial_vector(template, letters_pairs, num_pairs):
    template_pairs_position = [letters_pairs.index(xx) for xx in get_letters_pairs_str(template)]
    arr = np.zeros(num_pairs, dtype=int, order='C')
    for i in template_pairs_position:
        arr[i] = 1
    return arr

def pairs_to_num_dict(explicit_rules_dict, letters_pairs):
    explicit_rules_positions = {}
    for xy, xz_and_zy in explicit_rules_dict.items():
        xy_idx = letters_pairs.index(xy)
        xz_idx = letters_pairs.index(xz_and_zy[0])
        zy_idx = letters_pairs.index(xz_and_zy[1])
        explicit_rules_positions[xy_idx] = [xz_idx,zy_idx]
    return explicit_rules_positions

def create_adjacency_matrix(explicit_rules_positions, num_pairs):
    # if i --> j,k it means that there is a 1 in positions (j,i) and (k,i)
    matrix = np.zeros([num_pairs, num_pairs], dtype=int, order='C')
    for i, j_and_k in explicit_rules_positions.items():
        j = j_and_k[0]
        k = j_and_k[1]
        matrix[j,i] = 1
        matrix[k,i] = 1
    return matrix

def sparse_matrix_to_power_times_vector(sparse_matrix, pow, vector):
    matrix = csr_matrix(sparse_matrix, dtype=np.int64)
    power_of_matrix = (matrix**pow).toarray()
    return power_of_matrix.dot(vector)

def pairs_distr_to_final_result(final_vector_pairs, letters_pairs, template):
    pairs_distr = zip(letters_pairs, final_vector_pairs)
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lett_distr = dict(zip(alphabet, [0]*len(alphabet)))
    
    last_first_letters = template[-1] + template[0]

    for yy, num in pairs_distr:
        if yy == last_first_letters:
            num += 1
        for x in alphabet:
            if x in yy and num > 0:
                yy_is_xx = (yy[0] == x and yy[1] == x)
                lett_distr[x] += num if not yy_is_xx else 2*num
    
    return diff_of_most_minus_least_common(lett_distr)/2

def problem2(template, insertion_rules, num_steps):
    rules_dict = insertion_rules_to_dict(insertion_rules)
    explicit_rules_dict = two_pairs_from_dict(rules_dict)
    letters_pairs = get_letters_pairs(template, explicit_rules_dict)
    num_pairs = len(letters_pairs)
    initial_vector = create_initial_vector(template, letters_pairs, num_pairs)
    explicit_rules_positions = pairs_to_num_dict(explicit_rules_dict, letters_pairs)
    adjacency_matrix = create_adjacency_matrix(explicit_rules_positions, num_pairs)
    final_vector_pairs = sparse_matrix_to_power_times_vector(adjacency_matrix, num_steps, initial_vector)
    return pairs_distr_to_final_result(final_vector_pairs, letters_pairs, template)
    
dir_path = get_dir()
template = read('template', dir_path)[0]
insertion_rules = read('insertion_rules', dir_path)
template_example = read('template_example', dir_path)[0]
insertion_rules_example = read('insertion_rules_example', dir_path)

test2 = problem2(template_example, insertion_rules_example, 40)
result_problem2 = problem2(template, insertion_rules, 40)
pass