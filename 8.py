#!/usr/bin/env python

# Read the input data from the file
import copy


with open('input8.txt', 'r') as f:
    nodes = [line.strip() for line in f]

def antinodes_for_antennae(position1, position2, xmax, ymax):
    print(f"Checkling lines for: {position1} and {position2}")
    ret = []
    y_diff = position1[0] - position2[0]
    x_diff = position1[1] - position2[1]
    # add y and x fidd to p1 and subtrict from p2
    an1 = (position1[0] + y_diff, position1[1] + x_diff)
    an2 = (position2[0] - y_diff, position2[1] - x_diff)
    # check if the antinodes are within the bounds
    if an1[0] >= 0 and an1[0] < ymax and an1[1] >= 0 and an1[1] < xmax:
       ret.append(an1)
    if an2[0] >= 0 and an2[0] < ymax and an2[1] >= 0 and an2[1] < xmax:
       ret.append(an2)

    print(f"    Antinodes: {ret}")
    return ret

def antinodes_for_antennae_part_2(position1, position2, xmax, ymax):
    print(f"Checkling lines for: {position1} and {position2}")
    ret = []
    y_diff = position1[0] - position2[0]
    x_diff = position1[1] - position2[1]
    an1 = copy.copy(position1)
    ret.append(an1)
    while 1:
        an1 = (an1[0] + y_diff, an1[1] + x_diff)
        if an1[0] < 0 or an1[0] >= ymax or an1[1] < 0 or an1[1] >= xmax:
            break
        ret.append(an1)
    an2 = copy.copy(position2)
    ret.append(an2)
    while 1:
        an2 = (an2[0] - y_diff, an2[1] - x_diff)
        if an2[0] < 0 or an2[0] >= ymax or an2[1] < 0 or an2[1] >= xmax:
            break
        ret.append(an2)

    print(f"    Antinodes: {ret}")
    return ret

antennae_map = {}
for i in range(len(nodes)):
    for j in range(len(nodes[0])):
        if nodes[i][j] == ".":
            continue
        if nodes[i][j] not in antennae_map:
            antennae_map[nodes[i][j]] = []
        antennae_map[nodes[i][j]].append((i, j))

all_nodes = set()
for antennae, locations in antennae_map.items():
    for i in range(0, len(locations) - 1):
        for j in range(i + 1, len(locations)):
            all_nodes.update(antinodes_for_antennae(locations[i], locations[j], len(nodes[0]), len(nodes)))
    
print(len(all_nodes))

all_nodes = set()
for antennae, locations in antennae_map.items():
    for i in range(0, len(locations) - 1):
        for j in range(i + 1, len(locations)):
            all_nodes.update(antinodes_for_antennae_part_2(locations[i], locations[j], len(nodes[0]), len(nodes)))
    
print(all_nodes)
print(len(all_nodes))