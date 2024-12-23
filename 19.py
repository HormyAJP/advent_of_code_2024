#!/usr/bin/env python

CASE = 1
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
can_be_matched = {}

def iterate_mk2(pattern, primitives):
    if pattern == '':
        return 1
    if pattern in cant_be_matched:
        return 0
    if pattern in can_be_matched:
        return can_be_matched[pattern]
    
    total_ways = 0
    for primitive in primitives:
        if not pattern.startswith(primitive):
            continue
        total_ways += iterate_mk2(pattern[len(primitive):], primitives)
    can_be_matched[pattern] = total_ways
    if total_ways == 0:
        cant_be_matched.add(pattern)
    return total_ways

answer1 = 0
answer2 = 0

for desired_pattern in desired_patterns:
    ways_to_match = iterate_mk2(desired_pattern, available_patterns)
    if ways_to_match > 0:
        answer1 += 1
    answer2 += ways_to_match
print(f"Part 1: {answer1}, Part 2 {answer2}")
