#!/usr/bin/env python
import copy
from enum import Enum
import os
import numpy as np

CASE = 0
match CASE:
    case 0:
        input_file = 'input19_test_case_1.txt'
    case 1:
        input_file = 'input19.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    it = iter(f.readlines())
    available_patterns = [pattern.strip() for pattern in next(it).split(",")]
    next(it)
    desired_patterns = []
    for line in it:
        desired_patterns.append(line.strip())

cant_be_matched = set()

def iterate(pattern, index, matches_and_combinations, depth=0):
    if index == 0:
        return 1    
    # print(f"Depth: {depth}, matching {pattern[0:index]}")
    # keys = list(can_be_matched.keys())
    # keys.sort(reverse=True)
    to_match = pattern[0:index]
    if to_match in cant_be_matched:
        return 0
    # start_ways_to_match = ways_to_match
    ways_to_match_this_pattern = 0
    local_matches_and_combinations = copy.deepcopy(matches_and_combinations)
    for ap, ways in local_matches_and_combinations.items():
        # if len(ap) > index:
        #     continue
        # local_can_be_matched = can_be_matched[key]
        # for ap in local_can_be_matched:
        if to_match.endswith(ap):
            index_new = index - len(ap)
            previously_matched = pattern[index:]
            full_match = pattern[index_new:]
            assert(full_match not in matches_and_combinations)
            matches_and_combinations[full_match] = matches_and_combinations[previously_matched] * ways
            ways_to_match_this_pattern += iterate(pattern, index_new, matches_and_combinations, depth+1) * ways
    if ways_to_match_this_pattern == 0:
        cant_be_matched.add(to_match)
    return ways_to_match_this_pattern

def initialize_matches_and_combinations(available_patterns):
    matches_and_combinations = {}
    for ap in available_patterns:
        if len(ap) == 1:
            matches_and_combinations[ap] = 1

    max_len = max([len(ap) for ap in available_patterns])
    for i in range(2, max_len+1):
        for ap in available_patterns:
            if len(ap) != i:
                continue
            matches_and_combinations[ap] = iterate(ap, len(ap), matches_and_combinations)
    return matches_and_combinations

answer1 = 0
answer2 = 0
matches_and_combinations = initialize_matches_and_combinations(available_patterns)
for desired_pattern in desired_patterns:
    ways_to_match = iterate(desired_pattern, len(desired_pattern), matches_and_combinations)
    if ways_to_match > 0:
        answer1 += 1
    answer2 += ways_to_match
print(f"Total matches: {answer1}, Total count of matches {answer2}")
