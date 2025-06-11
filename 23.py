#!/usr/bin/env python

import collections
import copy
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

computers_to_connections = {}
for connection in connections:
    if connection[0] not in computers_to_connections:
        computers_to_connections[connection[0]] = []
    if connection[1] not in computers_to_connections:
        computers_to_connections[connection[1]] = []
    computers_to_connections[connection[0]].append(connection[1])
    computers_to_connections[connection[1]].append(connection[0])

for value in computers_to_connections.values():
    assert(len(set(value)) == len(value))

def deduplicate(maximal_subsets):
    deduped = set()    
    for maximal_subset in maximal_subsets:
        l = list(maximal_subset)
        l.sort()
        deduped.add(tuple(l))
    return [set(x) for x in deduped]

def iterate(computers_to_connections, connection_pairs, stop_size=-1):
    maximal_subsets = copy.deepcopy(connection_pairs)
    current_size = 2
    while 1:
        new_maximal_subsets = []
        for subset in maximal_subsets:
            for computer in computers_to_connections.keys():
                if computer in subset:
                    continue
                
                found = True
                for element in subset:
                    if element not in computers_to_connections[computer]:
                        found = False
                        break
                if found:
                    new_maximal_subsets.append(subset.union({computer}))
        
        new_maximal_subsets = deduplicate(new_maximal_subsets)
        current_size += 1
        if current_size == stop_size:
            return new_maximal_subsets
        if len(new_maximal_subsets) == 0:
            return maximal_subsets
        maximal_subsets = new_maximal_subsets


maximal = iterate(computers_to_connections, connection_pairs)
if len(maximal) != 1:
    for m in maximal:
        print(m)
    sys.exit(1)

maximal = maximal[0]
l = list(maximal)
l.sort()
print(",".join(l))
        


