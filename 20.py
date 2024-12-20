#!/usr/bin/env python

import copy
from enum import Enum
import os
import sys

CASE = 1
match CASE:
    case 0:
        input_file = 'input20_test_case_1.txt'
    case 1:
        input_file = 'input20.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    grid = []
    for line in f.readlines():
        grid.append(list(line.strip()))

def dump_paths(grid, paths):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            found_o = False
            for path in paths:
                if (x, y) in path.history:
                    found_o = True
                    
                    break
            if found_o:
                print("O", end="")
            else:
                print(cell, end="")
        print("")

# Firstly, solve the maze and record the numnber of steps to each point

def find_start(grid):
    start = None
    end = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                start = (x, y)
    return start

def surrouning_points(grid, point):
    x, y = point
    return [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]

def solve_maze(grid, start):
    current = start
    steps = 0
    visited = set()
    while 1:
        for point in surrouning_points(grid, current):
            if point in visited:
                continue
            match grid[point[1]][point[0]]:
                case "E":
                    grid[current[1]][current[0]] = steps
                    grid[point[1]][point[0]] = steps + 1
                    print(f"Steps to solve {steps + 1}")
                    return point
                case ".":
                    grid[current[1]][current[0]] = steps
                    steps += 1
                    current = point
                    visited.add(point)
                    break
                case "#":
                    continue

def take_shortcut(grid, shortcut1, previous_score, end):
    time_saves = []
    for point_around_shortcut1 in surrouning_points(grid, shortcut1):
        # No point taking shortcuts on the outside of the grid
        if point_around_shortcut1[0] == 0 or point_around_shortcut1[0] == len(grid[0]) - 1:
            continue
        if point_around_shortcut1[1] == 0 or point_around_shortcut1[1] == len(grid) - 1:
            continue        

        x = grid[point_around_shortcut1[1]][point_around_shortcut1[0]]
        match x:
            case "#":
                continue
                # shortcut2 = point_around_shortcut1
                # for point_around_shortcut2 in surrouning_points(grid, shortcut2):
                #     if point_around_shortcut2 == shortcut1:
                #         continue
                #     y = grid[point_around_shortcut2[1]][point_around_shortcut2[0]]
                #     match y:                    
                #         case "#":
                #             continue
                #         case int():
                #             y = int(y)
                #             score_with_shortcut = previous_score + 3
                #             if score_with_shortcut < y:
                #                 new_save = y - score_with_shortcut      
                #                 if new_save == 64:
                #                     pass                                                        
                #                 time_saves.append(new_save)
                #         case _:
                #             dump_paths(grid, [])
                #             assert(False)
            case int():
                x = int(x)
                score_with_shortcut = previous_score + 2
                if score_with_shortcut < x:
                    new_save = x - score_with_shortcut
                    if new_save == 64:
                        pass
                    time_saves.append(new_save)
            case _:
                assert(False)                    
    return time_saves

def diamond_of_surrounding_points(grid, point, size, base_steps):
    diamond  = {}
    centerx = point[0]
    centery = point[1]
    for x in range(0, size + 1):
        for y in range(0, size + 1):
            steps = x + y
            if steps >= size or steps == 0:
                continue
            possible_points = [
                (centerx + x, centery + y),
                (centerx + x, centery - y),
                (centerx - x, centery + y),
                (centerx - x, centery - y),
            ]
            for possible_point in possible_points:
                xpos = possible_point[0]
                ypos = possible_point[1]
                if xpos < 0 or ypos < 0 or xpos >= len(grid[0]) or ypos >= len(grid):
                    continue
                diamond[possible_point] = base_steps + steps
    return diamond 

def add_diamond_to_grid(grid, diamond):
    for point, value in diamond.items():
        grid[point[1]][point[0]] = value

# test_grid = copy.deepcopy(grid)
# test_diamond = diamond_of_surrounding_points(test_grid, (1, 3), 3, 0)
# add_diamond_to_grid(test_grid, test_diamond)
# dump_paths(test_grid, [])
# sys.exit(0)


def iterate_short_cuts(grid, start, end, cheat_time):
    current = start
    time_saves = []
    while current != end:
        current_score = grid[current[1]][current[0]]
        diamond = diamond_of_surrounding_points(grid, current, cheat_time, current_score)
        for point, steps in diamond.items():
            x = grid[point[1]][point[0]]
            match x:
                case "#":
                    continue
                case int():
                    x = int(x)
                    if steps < x:
                        time_saves.append(x - steps)
                case _:
                    assert(False)
        for point in surrouning_points(grid, current):
            if grid[point[1]][point[0]] == current_score + 1:
                current = point
                break
    return time_saves
    
start = find_start(grid)
end = solve_maze(grid, start)


time_saves = iterate_short_cuts(grid, start, end, 3)
print(len([x for x in time_saves if x >= 100]))

if CASE == 0:
    assert(time_saves.count(2) == 14)
    assert(time_saves.count(4) == 14)
    assert(time_saves.count(6) == 2)
    assert(time_saves.count(8) == 4)
    assert(time_saves.count(10) == 2)
    assert(time_saves.count(12) == 3)
    assert(time_saves.count(20) == 1)
    assert(time_saves.count(36) == 1)
    assert(time_saves.count(38) == 1)
    assert(time_saves.count(40) == 1)
    assert(time_saves.count(64) == 1)
    assert(set(time_saves) ==  {2, 4, 6, 8, 10, 12, 20, 36, 38, 40, 64})

time_saves = iterate_short_cuts(grid, start, end, 21)
print(len([x for x in time_saves if x >= 100]))

if CASE == 0:
    assert(time_saves.count(50) == 32)
    assert(time_saves.count(52) == 31)
    assert(time_saves.count(54) == 29)
    assert(time_saves.count(56) == 39)
    assert(time_saves.count(58) == 25)
    assert(time_saves.count(60) == 23)
    assert(time_saves.count(62) == 20)
    assert(time_saves.count(64) == 19)
    assert(time_saves.count(66) == 12)
    assert(time_saves.count(68) == 14)
    assert(time_saves.count(70) == 12)
    assert(time_saves.count(72) == 22)
    assert(time_saves.count(74) == 4)
    assert(time_saves.count(76) == 3)

