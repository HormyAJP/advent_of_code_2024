#!/usr/bin/env python

import collections
import functools
import itertools
import sys
import time

CASE = 1
match CASE:
    case 0:
        input_file = 'input23_test_case_1.txt'
    case 1:
        input_file = 'input23.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    connections = [line.strip().split('-') for line in f.readlines()]

connection_pairs = []
for connection in connections:
    connection_pairs.append(set(connection))

# all_computers = set()
# for connection in connections:
#     all_computers.add(connection[0])
#     all_computers.add(connection[1])

# print(f"Total computers: {len(all_computers)}")

# def build_lans(connections):
#     lans = []
#     lans_to_merge = []
#     remaining_lans = []    
#     for connection in connections:
#         lans = remaining_lans
#         remaining_lans = []
#         lans_to_merge = []

#         for lan in lans:
#             if connection[0] in lan or connection[1] in lan:
#                 lans_to_merge.append(lan)
#             else:
#                 remaining_lans.append(lan)
#         if lans_to_merge:
#             new_lan = set()
#             for lan in lans_to_merge:
#                 new_lan.update(lan)
#             new_lan.add(connection[0])
#             new_lan.add(connection[1])
#             remaining_lans.append(new_lan)
#         else:
#             new_lan = set()
#             new_lan.add(connection[0])
#             new_lan.add(connection[1])
#             remaining_lans.append(new_lan)
#     return lans

# def create_sets_of_3(lan):
#     print(f"Finding combos for {lan}")
#     ret = set()
#     for comb in itertools.combinations(lan, 3):
#         okay = False
#         for c in comb:
#             if c.startswith('t'):
#                 okay = True
#                 break
#         if not okay:
#             continue
#         # Convert c to a list
#         comb = list(comb)
#         comb.sort()
#         ret.add(tuple(comb))
#     for x in ret:
#         print(f"    {x}")
#     return ret

# lans = build_lans(connections)

def find_triples(connection_pairs):
    triples = []
    for first_pair in connection_pairs:
        for second_pair in connection_pairs:
            if len(first_pair.intersection(second_pair)) != 1:
                continue
            triple = first_pair.union(second_pair)
            missing_pair = triple - first_pair.intersection(second_pair)
            if missing_pair not in connection_pairs:
                continue
            if triple not in triples:
                triples.append(triple)
    return triples

good_triples = []
for t in find_triples(connection_pairs):
    okay = False
    for x in t:
        if x.startswith('t'):
            okay = True
            break
    if okay:
        good_triples.append(t)

print(len(good_triples))



# for lan in lans:
#     all_combos = set()
#     if len(lan) < 3:
#         continue
#     combos = create_sets_of_3(lan)
#     all_combos.update(combos)

# print(len(all_combos))
