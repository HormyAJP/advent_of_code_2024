#!/usr/bin/env python

with open('input10.txt', 'r') as f:
    top_map = [[int(num) for num in line.strip()] for line in f]

def check_trails(top_map, start):
    print(f"Checking trails for: {start}")
    found_peaks = set()
    routes = [start]
    while len(routes) > 0:
        new_routes = []
        for route in routes:
            y, x = route
            if x > 0:
                if top_map[y][x] == 8:
                    if top_map[y][x - 1] == 9:
                        found_peaks.add((y, x - 1))
                elif top_map[y][x - 1] == top_map[y][x] + 1:
                    new_routes.append((y, x - 1))
            if x < len(top_map[0]) - 1:
                if top_map[y][x] == 8:
                    if top_map[y][x + 1] == 9:
                        found_peaks.add((y, x + 1))
                elif top_map[y][x + 1] == top_map[y][x] + 1:
                    new_routes.append((y, x + 1))
            if y > 0:
                if top_map[y][x] == 8:
                    if top_map[y - 1][x] == 9:
                        found_peaks.add((y - 1, x))
                elif top_map[y - 1][x] == top_map[y][x] + 1:
                    new_routes.append((y - 1, x))
            if y < len(top_map) - 1:
                if top_map[y][x] == 8:
                    if top_map[y + 1][x] == 9:
                        found_peaks.add((y + 1, x))
                elif top_map[y + 1][x] == top_map[y][x] + 1:
                    new_routes.append((y + 1, x))
        routes = new_routes
    return len(found_peaks)

# Could have easily combined the two functions
def check_trails2(top_map, start):
    print(f"Checking trails for: {start}")
    found_peaks = []
    routes = [start]
    while len(routes) > 0:
        new_routes = []
        for route in routes:
            y, x = route
            if x > 0:
                if top_map[y][x] == 8:
                    if top_map[y][x - 1] == 9:
                        found_peaks.append((y, x - 1))
                elif top_map[y][x - 1] == top_map[y][x] + 1:
                    new_routes.append((y, x - 1))
            if x < len(top_map[0]) - 1:
                if top_map[y][x] == 8:
                    if top_map[y][x + 1] == 9:
                        found_peaks.append((y, x + 1))
                elif top_map[y][x + 1] == top_map[y][x] + 1:
                    new_routes.append((y, x + 1))
            if y > 0:
                if top_map[y][x] == 8:
                    if top_map[y - 1][x] == 9:
                        found_peaks.append((y - 1, x))
                elif top_map[y - 1][x] == top_map[y][x] + 1:
                    new_routes.append((y - 1, x))
            if y < len(top_map) - 1:
                if top_map[y][x] == 8:
                    if top_map[y + 1][x] == 9:
                        found_peaks.append((y + 1, x))
                elif top_map[y + 1][x] == top_map[y][x] + 1:
                    new_routes.append((y + 1, x))
        routes = new_routes
    return len(found_peaks)

answer1 = 0
for y in range(len(top_map)):
    for x in range(len(top_map[0])):
        if top_map[y][x] == 0:
            answer1 += check_trails(top_map, (y, x))
print(answer1)

answer2 = 0
for y in range(len(top_map)):
    for x in range(len(top_map[0])):
        if top_map[y][x] == 0:
            answer2 += check_trails2(top_map, (y, x))
print(answer2)