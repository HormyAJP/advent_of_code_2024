#!/usr/bin/env python
import copy
from enum import Enum
import os
import sys
import time
import numpy as np
import re

CASE = 2

match CASE:
    case 0:
        input_file = 'input16_test_case1.txt'
    case 1:
        input_file = 'input16_test_case2.txt'
    case 2:
        input_file = 'input16.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    grid = []
    for line in f.readlines():
        grid.append(list(line.strip()))


class Direction(Enum):
    UP = "^"
    DOWN = "V"
    LEFT = "<"
    RIGHT = ">"

def rotate(direction, clockwise=True):
    if clockwise:
        match direction:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP
    else:
        match direction:
            case Direction.UP:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.UP


class PathHead:

    def __init__(self, position, direction, score, history=None):
        self.position = position
        self.direction = direction
        self.score = score
        if history is None:    
            self.history = []
        else:
            self.history = copy.deepcopy(history)

    def move(self, direction):
        if direction == Direction.UP:
            return PathHead((self.position[0], self.position[1] - 1), direction, self.score + 1, self.history + [self.position])
        elif direction == Direction.DOWN:
            return PathHead((self.position[0], self.position[1] + 1), direction, self.score + 1, self.history + [self.position])
        elif direction == Direction.LEFT:
            return PathHead((self.position[0] - 1, self.position[1]), direction, self.score + 1, self.history + [self.position])
        elif direction == Direction.RIGHT:
            return PathHead((self.position[0] + 1, self.position[1]), direction, self.score + 1, self.history + [self.position])
        else:
            raise Exception("Unknown direction")
    
    def already_visited(self, position):
        if position in self.history:
            return True
        return False

    def rotate(self, clockwise=True):
        match self.direction:
            case Direction.UP:
                return PathHead(self.position, rotate(self.direction, clockwise), self.score + 1000, self.history + [(self.position[0], self.position[1] + 1), (self.position[0], self.position[1] - 1)])
            case Direction.DOWN:
                return PathHead(self.position, rotate(self.direction, clockwise), self.score + 1000, self.history + [(self.position[0], self.position[1] + 1), (self.position[0], self.position[1] - 1)])
            case Direction.LEFT:
                return PathHead(self.position, rotate(self.direction, clockwise), self.score + 1000, self.history + [(self.position[0] + 1, self.position[1]), (self.position[0] - 1, self.position[1])])
            case Direction.RIGHT:
                return PathHead(self.position, rotate(self.direction, clockwise), self.score + 1000, self.history + [(self.position[0] + 1, self.position[1]), (self.position[0] - 1, self.position[1])])
    
    def __str__(self):
        return f"PathHead({self.position}, {self.direction}, {self.score})"


# We will evolve the maxe using A* search. However, we don't stop once the first 
# solution is found. We keep going until there are no active paths whose score is
# less than the best score found so far. 

def dump_heads(grid, heads):
    os.system("clear")
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if any([head.position == (x, y) for head in heads]):
                print("X", end="")
            else:
                print(cell, end="")
        print("")

def astar_solve_maze(grid, active_paths):
    best_score = sys.maxsize
    while active_paths:
        dump_heads(grid, active_paths)
        print(f"Num active paths: {len(active_paths)}")
        new_active_paths = []
        for active_path in active_paths:
            match active_path.direction:
                case Direction.UP:
                    if grid[active_path.position[1] - 1][active_path.position[0]] == "E":
                        best_score = min(best_score, active_path.score + 1)
                        continue                    
                    if grid[active_path.position[1] - 1][active_path.position[0]] == ".":
                        if active_path.score + 1 < best_score:
                            new_position = (active_path.position[0], active_path.position[1] - 1)
                            if not active_path.already_visited(new_position):
                                new_active_paths.append(active_path.move(Direction.UP))
                    if active_path.score + 1000 >= best_score:
                        continue
                    if grid[active_path.position[1]][active_path.position[0] - 1] == ".":
                        new_position = (active_path.position[0] - 1, active_path.position[1])
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=False))
                    if grid[active_path.position[1]][active_path.position[0] + 1] == ".":
                        new_position = (active_path.position[0] + 1, active_path.position[1])
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=True))
                case Direction.DOWN:
                    if grid[active_path.position[1] + 1][active_path.position[0]] == "E":
                        best_score = min(best_score, active_path.score + 1)
                        continue                    
                    if grid[active_path.position[1] + 1][active_path.position[0]] == ".":
                        if active_path.score + 1 < best_score:
                            new_position = (active_path.position[0], active_path.position[1] + 1)
                            if not active_path.already_visited(new_position):
                                new_active_paths.append(active_path.move(Direction.DOWN))
                    if active_path.score + 1000 >= best_score:
                        continue
                    if grid[active_path.position[1]][active_path.position[0] - 1] == ".":
                        new_position = (active_path.position[0] - 1, active_path.position[1])
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=True))
                    if grid[active_path.position[1]][active_path.position[0] + 1] == ".":
                        new_position = (active_path.position[0] + 1, active_path.position[1])
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=False))
                case Direction.LEFT:
                    if grid[active_path.position[1]][active_path.position[0] - 1] == "E":
                        best_score = min(best_score, active_path.score + 1)
                        continue                    
                    if grid[active_path.position[1]][active_path.position[0] - 1] == ".":
                        if active_path.score + 1 < best_score:
                            new_position = (active_path.position[0] - 1, active_path.position[1])
                            if not active_path.already_visited(new_position):
                                new_active_paths.append(active_path.move(Direction.LEFT))
                    if active_path.score + 1000 >= best_score:
                        continue
                    if grid[active_path.position[1] - 1][active_path.position[0]] == ".":
                        new_position = (active_path.position[0], active_path.position[1] - 1)
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=True))
                    if grid[active_path.position[1] + 1][active_path.position[0]] == ".":
                        new_position = (active_path.position[0], active_path.position[1] + 1)
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=False))
                case Direction.RIGHT:
                    if grid[active_path.position[1]][active_path.position[0] + 1] == "E":
                        best_score = min(best_score, active_path.score + 1)
                        continue                    
                    if grid[active_path.position[1]][active_path.position[0] + 1] == ".":
                        if active_path.score + 1 < best_score:
                            new_position = (active_path.position[0] + 1, active_path.position[1])
                            if not active_path.already_visited(new_position):
                                new_active_paths.append(active_path.move(Direction.RIGHT))
                    if active_path.score + 1000 >= best_score:
                        continue
                    if grid[active_path.position[1] - 1][active_path.position[0]] == ".":
                        new_position = (active_path.position[0], active_path.position[1] - 1)
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=False))
                    if grid[active_path.position[1] + 1][active_path.position[0]] == ".":
                        new_position = (active_path.position[0], active_path.position[1] + 1)
                        if not active_path.already_visited(new_position):
                            new_active_paths.append(active_path.rotate(clockwise=True))
        minima = {}
        for path in new_active_paths:
            if path.position in minima:
                if path.score < minima[path.position].score:
                    minima[path.position] = path
            else:
                minima[path.position] = path
        new_active_paths = list(minima.values())
        active_paths = new_active_paths
    return best_score

s_position = (1, len(grid) - 2)
assert(grid[s_position[1]][s_position[0]] == "S")
active_paths = [PathHead(s_position, Direction.RIGHT, 0)]

score = astar_solve_maze(grid, active_paths)
print(score)