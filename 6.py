#!/usr/bin/env python

# Gemini couldn't handle this one. 
# First part was easy. Second I just brute forced. Not a big issue 
# given the input size.

import copy
from enum import Enum
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class StuckInLoop(Exception):
    pass

# Read the input from a file
with open('input6.txt', 'r') as f:
    grid = [list(line.strip()) for line in f]

def find_start_position(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == '^':
                return x, y

def simulate_guard(grid):
    x, y = find_start_position(grid)
    direction = Direction.UP

    visited = {}
    while 1:
        if (x, y) not in visited:
            visited[(x, y)] = []
        else:
            if direction in visited[(x, y)]:
                raise StuckInLoop()
        visited[(x, y)].append(direction)
        if direction == Direction.UP:
            if y == 0:
                break
            if grid[y - 1][x] == '#':
                direction = Direction.RIGHT
                continue
            y -= 1
            continue
        elif direction == Direction.DOWN:
            if y == len(grid) - 1:
                break
            if grid[y + 1][x] == '#':
                direction = Direction.LEFT
                continue
            y += 1
            continue
        elif direction == Direction.LEFT:
            if x == 0:
                break
            if grid[y][x - 1] == '#':
                direction = Direction.UP
                continue
            x -= 1
            continue
        elif direction == Direction.RIGHT:
            if x == len(grid[y]) - 1:
                break
            if grid[y][x + 1] == '#':
                direction = Direction.DOWN
                continue
            x += 1
            continue
    return len(visited.keys())

# Simulate the guard's movement and count visited positions
num_positions = simulate_guard(grid)
print(num_positions)

count_of_loops = 0
for i in range(len(grid)):
    print(i)
    for j in range(len(grid[i])):
        if grid[i][j] != '.':
            continue
        new_grid = copy.deepcopy(grid)
        new_grid[i][j] = '#'
        try:
            simulate_guard(new_grid)
        except StuckInLoop as e:
            count_of_loops += 1
print(count_of_loops)