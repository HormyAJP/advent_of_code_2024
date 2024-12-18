#!/usr/bin/env python
import copy
from enum import Enum
import os
import numpy as np

# Code in this solution is gross. I cribbed it for 16.py and then just hacked it
# to make it work here. It's good enough. Gets the job done.

CASE = 1
match CASE:
    case 0:
        input_file = 'input18_test_case_1.txt'
        grid_size = (7,7)
        steps = 12
    case 1:
        input_file = 'input18.txt'        
        grid_size = (71,71)        
        steps = 1024
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    byte_coords = []
    for line in f.readlines():
        x,y = line.strip().split(",")
        byte_coords.append((int(x), int(y)))

class Direction(Enum):
    UP = "^"
    DOWN = "V"
    LEFT = "<"
    RIGHT = ">"

class PathHead:

    def __init__(self, position, direction, score, history=None):
        self.position = position
        self.direction = direction
        self.score = score
        if history is None:    
            self.history = []
        else:
            self.history = copy.deepcopy(history)

    def move(self, current_score, direction):
        if direction == Direction.UP:
            return PathHead((self.position[0], self.position[1] - 1), direction, current_score + 1, self.history + [self.position])
        elif direction == Direction.DOWN:
            return PathHead((self.position[0], self.position[1] + 1), direction, current_score + 1, self.history + [self.position])
        elif direction == Direction.LEFT:
            return PathHead((self.position[0] - 1, self.position[1]), direction, current_score + 1, self.history + [self.position])
        elif direction == Direction.RIGHT:
            return PathHead((self.position[0] + 1, self.position[1]), direction, current_score + 1, self.history + [self.position])
        else:
            raise Exception("Unknown direction")

    def __str__(self):
        return f"PathHead({self.position}, {self.direction}, {self.score})"


def dump_heads(grid, heads):
    os.system("clear")
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            val = 0
            for head in heads:
                if head.position == (x, y):
                    if val == 0:
                        val = head.score
                    elif int(head.score) < val:
                        val = head.score
            if val != 0:
                print(val, end="")
            else:
                print(cell, end="")
        print("")

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

def astar_solve_maze(grid, scores, head):
    active_paths = [head]
    scores[head.position[1]][head.position[0]] = 0

    while active_paths:
        # dump_heads(grid, active_paths)
        # print(f"Num active paths: {len(active_paths)}")
        new_active_paths = []
        for active_path in active_paths:
            all_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            next_paths = [active_path.move(active_path.score, direction) for direction in all_directions]                
            for next_path in next_paths:                
                next_square_value = grid[next_path.position[1]][next_path.position[0]]
                if next_square_value == "#":
                    continue                
                   
                if next_square_value == "E":
                    return next_path.score
                
                if scores[next_path.position[1]][next_path.position[0]] == ".":
                    scores[next_path.position[1]][next_path.position[0]] = str(next_path.score)
                    new_active_paths.append(next_path)
                else:
                    if next_path.score < int(scores[next_path.position[1]][next_path.position[0]]):
                        scores[next_path.position[1]][next_path.position[0]] = str(next_path.score)
                        new_active_paths.append(next_path)
                
        active_paths = new_active_paths                   

    raise Exception("FAILED TO SOLVE")

def build_grid(grid_size, byte_coords, add_end=True):
    grid = np.full((grid_size[1]+2, grid_size[0]+2), ".")
    for x,y in byte_coords:
        grid[y+1][x+1] = "#"
    if add_end:
        grid[grid_size[1]][grid_size[0]] = "E"
    
    # Surround with walls to reuse old code
    grid[0, :] = "#"
    grid[:, 0] = "#"
    grid[grid_size[1]+1, :] = "#"
    grid[:, grid_size[0]+1] = "#"
    return grid

# Uncomment for part 1.
# grid = build_grid(grid_size, byte_coords[0:steps])
# scores = build_grid(grid_size, [])
# dump_paths(scores, [PathHead((1,1), Direction.RIGHT, 0)])
# print(astar_solve_maze(grid, scores, PathHead((1,1), Direction.RIGHT, 0)))


# Binary chop to find bad bye
lgood = 0
rbad = len(byte_coords)
index = len(byte_coords)  // 2
while True:
    grid = build_grid(grid_size, byte_coords[0:index])
    scores = build_grid(grid_size, [], add_end=False)
    try:
        astar_solve_maze(grid, scores, PathHead((1,1), Direction.RIGHT, 0))
        lgood = index
    except Exception as e:
        rbad = index
    if lgood == rbad - 1:
        print(f"Bad index {rbad-1}: Bad byte {byte_coords[rbad-1]}")
        break
    index = (rbad - lgood) // 2 + lgood
    