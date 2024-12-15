#!/usr/bin/env python
import copy
import os
import time
import numpy as np
import re

CASE = 3

match CASE:
    case 0:
        input_file = 'input15_test_case_1.txt'
    case 1:
        input_file = 'input15_test_case_2.txt'
    case 2:
        input_file = 'input15_test_case_3.txt'
    case 3:
        input_file = 'input15.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    grid = []
    it = iter(f.readlines())
    robot = None
    y = 0
    while 1:
        line = next(it).strip()
        if len(line) == 0 or line[0] != "#":
            break
        if "@" in line:
            assert(robot is None)
            robot = (line.index("@"), y)
        grid.append(list(line))
        y += 1
    
    assert(robot is not None)
    
    commands = ""
    try:
        while 1:
            line = next(it).strip()
            commands += line
    except StopIteration:
        pass

original_grid = copy.deepcopy(grid)

def dump_grid(grid):
    for row in grid:
        print("".join(row))

# These functions look a bit grim. But copilot helped do the duplication so
# I got lazy and left them like this.
def move_object_right(grid, object, test_only=False):
    object_type = grid[object[1]][object[0]]
    assert(object_type in ["@", "O", "[", "]"])
    if grid[object[1]][object[0]+1] == ".":
        if not test_only:
            grid[object[1]][object[0]+1] = object_type
            grid[object[1]][object[0]] = "."
        return True
    elif grid[object[1]][object[0]+1] == "#":
        return False
    elif grid[object[1]][object[0]+1] in ["O", "[", "]"]:
        if move_object_right(grid, (object[0]+1, object[1]), test_only):
            if not test_only:
                assert(grid[object[1]][object[0]+1] == ".")
                grid[object[1]][object[0]+1] = object_type
                grid[object[1]][object[0]] = "."
            return True
        return False
    assert(False)

def move_object_left(grid, object, test_only=False):
    object_type = grid[object[1]][object[0]]
    assert(object_type in ["@", "O", "[", "]"])
    if grid[object[1]][object[0]-1] == ".":
        if not test_only:
            grid[object[1]][object[0]-1] = object_type
            grid[object[1]][object[0]] = "."
        return True
    elif grid[object[1]][object[0]-1] == "#":
        return False
    elif grid[object[1]][object[0]-1] in ["O", "[", "]"]:
        if move_object_left(grid, (object[0]-1, object[1]), test_only):
            if not test_only:
                assert(grid[object[1]][object[0]-1] == ".")
                grid[object[1]][object[0]-1] = object_type
                grid[object[1]][object[0]] = "."
            return True
        return False
    assert(False)

def move_object_up(grid, object, test_only=False):
    object_type = grid[object[1]][object[0]]
    next_object = grid[object[1]-1][object[0]]
    assert(object_type in ["@", "O", "[", "]"])
    if next_object == ".":
        if not test_only:
            grid[object[1]-1][object[0]] = object_type
            grid[object[1]][object[0]] = "."
        return True
    elif next_object == "#":
        return False
    elif next_object == "O":
        if move_object_up(grid, (object[0], object[1]-1)):
            if not test_only:
                assert(grid[object[1]-1][object[0]] == ".")
                grid[object[1]-1][object[0]] = object_type
                grid[object[1]][object[0]] = "."
            return True
        return False
    elif next_object in ["[", "]"]:
        can_move = move_object_up(grid, (object[0], object[1]-1), test_only)
        if next_object == "[":
            can_move = can_move and move_object_up(grid, (object[0]+1, object[1]-1), test_only)
        elif next_object == "]":
            can_move = can_move and move_object_up(grid, (object[0]-1, object[1]-1), test_only)
        if not can_move:
            return False
        if not test_only:
            assert(grid[object[1]-1][object[0]] == ".")
            grid[object[1]-1][object[0]] = object_type
            grid[object[1]][object[0]] = "."            
        return True
    assert(False)

def move_object_down(grid, object, test_only=False):
    object_type = grid[object[1]][object[0]]
    next_object = grid[object[1]+1][object[0]]
    assert(object_type in ["@", "O", "[", "]"])
    if next_object == ".":
        if not test_only:
            grid[object[1]+1][object[0]] = object_type
            grid[object[1]][object[0]] = "."
        return True
    elif next_object == "#":
        return False
    elif next_object == "O":
        if move_object_down(grid, (object[0], object[1]+1)):
            if not test_only:
                assert(grid[object[1]+1][object[0]] == ".")
                grid[object[1]+1][object[0]] = object_type
                grid[object[1]][object[0]] = "."
            return True
        return False
    elif next_object in ["[", "]"]:
        can_move = move_object_down(grid, (object[0], object[1]+1), test_only)
        if next_object == "[":
            can_move = can_move and move_object_down(grid, (object[0]+1, object[1]+1), test_only)
        elif next_object == "]":
            can_move = can_move and move_object_down(grid, (object[0]-1, object[1]+1), test_only)
        if not can_move:
            return False
        if not test_only:
            assert(grid[object[1]+1][object[0]] == ".")
            grid[object[1]+1][object[0]] = object_type
            grid[object[1]][object[0]] = "."            
        return True
    assert(False)

def find_robot(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "@":
                return (x, y)
    assert(False)

def evolve(grid, command):
    # dump_grid(grid)
    # print(f"\nMoving {command}\n\n")
    robot = find_robot(grid)
    match command:
        case ">":
            if move_object_right(grid, robot, test_only=True):
                move_object_right(grid, robot)
        case "<":
            if move_object_left(grid, robot, test_only=True):
                move_object_left(grid, robot)
        case "^":
            if move_object_up(grid, robot, test_only=True):
                move_object_up(grid, robot)
        case "v":
            if move_object_down(grid, robot, test_only=True):
                move_object_down(grid, robot)
        case _:
            raise Exception("Unknown command")

def sum_gps_coords(grid):
    sum = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell in ["O","["]:
                sum += x + 100*y
    return sum

def stretch_grid(grid):
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            match cell:
                case "#":
                    new_row += ["#"]*2
                case ".":
                    new_row += ["."]*2
                case "@":
                    new_row.append("@")
                    new_row.append(".")
                case "O":
                    new_row.append("[")
                    new_row.append("]")
                case _:
                    raise Exception("Unknown cell")
        new_grid.append(list(new_row))
    return new_grid

# Part 1
# for command in commands:
#     robot = evolve(grid, command)
# print(sum_gps_coords(grid))

# Part 2
grid = stretch_grid(original_grid)
dump_grid(grid)
for command in commands:
    robot = evolve(grid, command)

print(sum_gps_coords(grid))

# dump_grid(stretch_grid(grid))