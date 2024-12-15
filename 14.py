#!/usr/bin/env python
import os
import time
import numpy as np
import re

USE_TESTS_CASE=False

if USE_TESTS_CASE:
    grid_size=(11, 7)
    num_steps = 100
    input_file = 'input14_test_case.txt'
else:
    grid_size=(101, 103)
    num_steps = 100
    input_file = 'input14.txt'

class Robot:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def __str__(self):
        return f"Robot({self.x}, {self.y}, {self.vx}, {self.vy})"

    def __repr__(self):
        return self.__str__()
    
    def move(self, grid_size):
        self.x = (self.x + self.vx) % grid_size[0]
        self.y = (self.y + self.vy) % grid_size[1]

def print_robot_positions(robots, grid_size):
    os.system("clear")
    grid = np.full((grid_size[1], grid_size[0]), 0)
    for r in robots:
        grid[r.y, r.x] += 1
    for i in range(0, grid_size[1]):
        row = grid[i, :]
        row = ['.' if x == 0 else str(x) for x in row]
        print("".join(row))

# Part two was a bugger. I ended up just printing every frame and watching
# to get inspiration. I noticed that occasionally the robots would cluster
# non-centrally. I guessed that maybe the tree wasn't in the center of the
# image. So I started checking for arrangments where the mean was away
# from the center. The logic being that generally the robots will look 
# randomly arranged and so their mean will be about the middle.
# Using this I could step through more carefully until I found the tree.
# I thought I might need more than this but actually it only took
# 30s of stepping and I saw it.
def mean_is_not_central(robots, grid_size):
    count = 0
    x_total = 0
    for r in robots:
        x_total += r.x
        count += 1
    mean = x_total / count
    if mean > 60 or mean < 40:
        return True
    return False

with open(input_file, 'r') as f:
    robots = []
    prog = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")
    for line in f.readlines():
        m = prog.match(line)
        if not m:
            raise Exception("Invalid line")
        robots.append(Robot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

# Uncomment for part 1.
# for t in range(0, num_steps):
#     print_robot_positions(robots, grid_size)
#     print("="*80)    
#     for r in robots:
#         r.move(grid_size)
# print_robot_positions(robots, grid_size)

# # Ordered top left, top right, bottom left, bottom right
# quadrant_counts = [0,0,0,0]
# for r in robots:
#     if r.x < grid_size[0]//2 and r.y < grid_size[1]//2:
#         quadrant_counts[0] += 1
#     elif r.x > grid_size[0]//2 and r.y < grid_size[1]//2:
#         quadrant_counts[1] += 1
#     elif r.x < grid_size[0]//2 and r.y > grid_size[1]//2:
#         quadrant_counts[2] += 1
#     elif r.x > grid_size[0]//2 and r.y > grid_size[1]//2:
#         quadrant_counts[3] += 1

# print(math.prod(quadrant_counts))

# After 101*103=10303 iterations we're back where we started, so the 
# tree must appear in this range
for t in range(0, 101*103):
    [r.move(grid_size) for r in robots]
    if mean_is_not_central(robots, grid_size):
        print_robot_positions(robots, grid_size)
        print(t)    
        time.sleep(0.5)
        pass
    