#!/usr/bin/env python
import copy
from enum import Enum
import os
import sys
import numpy as np
import time

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

def opposite_direction(direction):
    match direction:
        case Direction.UP:
            return Direction.DOWN
        case Direction.DOWN:
            return Direction.UP
        case Direction.LEFT:
            return Direction.RIGHT
        case Direction.RIGHT:
            return Direction.LEFT

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
        if direction != self.direction:
            score = 1001
        else:
            score = 1
        if direction == Direction.UP:
            return PathHead((self.position[0], self.position[1] - 1), direction, self.score + score, self.history + [self.position])
        elif direction == Direction.DOWN:
            return PathHead((self.position[0], self.position[1] + 1), direction, self.score + score, self.history + [self.position])
        elif direction == Direction.LEFT:
            return PathHead((self.position[0] - 1, self.position[1]), direction, self.score + score, self.history + [self.position])
        elif direction == Direction.RIGHT:
            return PathHead((self.position[0] + 1, self.position[1]), direction, self.score + score, self.history + [self.position])
        else:
            raise Exception("Unknown direction")
    
    def already_visited(self, position):
        if position in self.history:
            return True
        return False

    def __str__(self):
        return f"PathHead({self.position}, {self.direction}, {self.score})"


# We will evolve the maxe using A* search. However, we don't stop once the first 
# solution is found. We keep going until there are no active paths whose score is
# less than the best score found so far. 

def dump_heads(grid, heads):
    os.system("clear")
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            count = sum([head.position == (x, y) for head in heads])
            if count:
                print(count, end="")
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

def astar_solve_maze(grid, head):
    best_score = sys.maxsize
    active_paths = [head]
    winning_paths = []
    visited_postions = {
        head.position: head.score
    }

    while active_paths:
        # dump_heads(grid, active_paths)
        # print(f"Num active paths: {len(active_paths)}")
        new_active_paths = []
        for active_path in active_paths:
            all_directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            all_directions.remove(opposite_direction(active_path.direction))
            next_paths = [active_path.move(direction) for direction in all_directions]                
            for next_path in next_paths:
                if next_path.score > best_score:
                    continue
                
                next_square_value = grid[next_path.position[1]][next_path.position[0]]
                if next_square_value == "#":
                    continue                
                
                # if (next_path.position, next_path.direction) in visited_postions and next_path.score > visited_postions[(next_path.position, next_path.direction)]:
                #     continue
                if next_path.position in visited_postions and next_path.score > visited_postions[next_path.position] + 1000:
                    continue                
                
                if next_square_value == "E":
                    if next_path.score == best_score:
                        winning_paths.append(next_path)
                    elif next_path.score < best_score:
                        best_score = next_path.score
                        winning_paths = [next_path]
                    continue
                
                new_active_paths.append(next_path)  
                visited_postions[next_path.position] = next_path.score

        active_paths = new_active_paths                   

    all_squares = set()
    for next_path in winning_paths:
        all_squares.update(next_path.history)
        all_squares.add(next_path.position)
    dump_paths(grid, winning_paths)
    return best_score, len(all_squares)

start = time.time()

s_position = (1, len(grid) - 2)
assert(grid[s_position[1]][s_position[0]] == "S")
score_and_num_visited_squares = astar_solve_maze(grid, PathHead(s_position, Direction.RIGHT, 0))
print(score_and_num_visited_squares)

end = time.time()
print(f"Time: {end-start}")