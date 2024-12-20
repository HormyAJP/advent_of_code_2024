#!/usr/bin/env python
import copy
from enum import Enum
import os
import numpy as np

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


can_be_matched = {}
cant_be_matched = set()

def iterate(pattern, index, depth=0):
    print(f"Depth: {depth}, matching {pattern[0:index]}")
    keys = list(can_be_matched.keys())
    # keys.sort(reverse=True)
    to_match = pattern[0:index]
    if to_match in cant_be_matched:
        return False
    for key in keys:
        if key > index:
            continue
        local_can_be_matched = can_be_matched[key]
        for ap in local_can_be_matched:
            if to_match.endswith(ap):
                index_new = index - len(ap)
                match_len = len(pattern) - index_new
                if match_len not in can_be_matched:
                    can_be_matched[match_len] = set()
                # print(f"Adding {pattern[index_new:len(pattern)]} to cache")
                can_be_matched[match_len].add(pattern[index_new:len(pattern)])
                if index_new == 0:
                    return True
                if iterate(pattern, index_new, depth+1):
                    return True
    cant_be_matched.add(to_match)

        

def match_pattern(pattern, available_patterns):
    print(f"Trying to match {pattern}")
    attempts = [len(pattern)]
    
    for ap in available_patterns:
        if len(ap) not in can_be_matched:
            can_be_matched[len(ap)] = set()
        can_be_matched[len(ap)].add(ap)
    
    return iterate(pattern, len(pattern))

total = 0
for desired_pattern in desired_patterns:
    if match_pattern(desired_pattern, available_patterns):
        total += 1
print(f"Total matches: {total}")
