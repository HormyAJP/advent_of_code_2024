#!/usr/bin/env python

with open('input12.txt', 'r') as f:
    grid = [l.strip() for l in f.readlines()]

def find_touching(grid, location):
    touching = []
    x, y = location
    label = grid[y][x]
    if x > 0 and grid[y][x-1] == label:
        touching.append((x-1, y))
    if x < len(grid[0])-1 and grid[y][x+1] == label:
        touching.append((x+1, y))
    if y > 0 and grid[y-1][x] == label:
        touching.append((x, y-1))
    if y < len(grid)-1 and grid[y+1][x] == label:
        touching.append((x, y+1))
    return touching

def find_area_and_permimeter(grid, start_location, visited):
    area = 1
    perimeter = 0
    current = [start_location]
    # print(grid[start_location[1]][start_location[0]])
    while current:
        next_current = []
        for x in current:
            touching = find_touching(grid, x)
            perimeter += 4 - len(touching)
            for t in touching:
                if t in visited:
                    continue
                area += 1
                next_current.append(t)
                visited.add(t)
        current = next_current
    # print(f"a: {area}, p: {perimeter}")
    return area * perimeter

def find_9x9_neighbours(grid, location):
    x, y = location
    char_to_match = grid[y][x]
    ret = [['O','O','O'], ['O','X','O'], ['O','O','O']]
    if x > 0:
        if grid[y][x-1] == char_to_match:
            ret[1][0] = 'X'
        if y > 0:
            if grid[y-1][x-1] == char_to_match:
                ret[0][0] = 'X'
        if y < len(grid) - 1:
            if grid[y+1][x-1] == char_to_match:
                ret[2][0] = 'X'       
    if x < len(grid[0]) - 1:
        if grid[y][x+1] == char_to_match:
            ret[1][2] = 'X'
        if y > 0:
            if grid[y-1][x+1] == char_to_match:
                ret[0][2] = 'X'
        if y < len(grid) - 1:
            if grid[y+1][x+1] == char_to_match:
                ret[2][2] = 'X'                   
    if y > 0:
        if grid[y-1][x] == char_to_match:
            ret[0][1] = 'X'                   
    if y < len(grid) - 1:
        if grid[y+1][x] == char_to_match:
            ret[2][1] = 'X'                           
    return ret

def dump_neighbours(neighbours):
    for i in range(0, len(neighbours)):
        print(neighbours[i])
    print("\n")

def neighbours_to_subsquares(neighbours):
    ret = []
    for i in range(0, 2):
        for j in range(0, 2):
            subsquares = [[None,None], [None,None]]
            subsquares[0][0] = neighbours[0+i][0+j]
            subsquares[0][1] = neighbours[0+i][1+j]
            subsquares[1][0] = neighbours[1+i][0+j]
            subsquares[1][1] = neighbours[1+i][1+j]
            ret.append(subsquares)
    return ret

def count_corners_in_neighbourhood(neighbours):
    # dump_neighbours(neighbours)
    count = 0
    assert(neighbours[1][1] == 'X')
    # Top left
    if neighbours[0][1] == 'O' and neighbours[1][0] == 'O':
        count += 1
    if neighbours[0][0] == 'O' and neighbours[1][0] == 'X' and neighbours[0][1] == 'X':
        count += 1
    # Top right
    if neighbours[0][1] == 'O' and neighbours[1][2] == 'O':
        count += 1
    if neighbours[0][2] == 'O' and neighbours[1][2] == 'X' and neighbours[0][1] == 'X':
        count += 1
    # Bottom left
    if neighbours[1][0] == 'O' and neighbours[2][1] == 'O':
        count += 1
    if neighbours[2][0] == 'O' and neighbours[1][0] == 'X' and neighbours[2][1] == 'X':
        count += 1
    # Bottom right
    if neighbours[1][2] == 'O' and neighbours[2][1] == 'O':
        count += 1
    if neighbours[2][2] == 'O' and neighbours[1][2] == 'X' and neighbours[2][1] == 'X':
        count += 1

    return count

def find_area_and_edges(grid, start_location, visited):
    area = 1
    corners = 0
    current = [start_location]
    # print(grid[start_location[1]][start_location[0]])
    while current:
        next_current = []
        for x in current:
            touching = find_touching(grid, x)
            neighbours = find_9x9_neighbours(grid, x)
            c = count_corners_in_neighbourhood(neighbours)
            corners += c
            for t in touching:
                if t in visited:
                    continue
                # corners += count_corners_in_neighbourhood(neighbours)
                area += 1
                next_current.append(t)
                visited.add(t)
        current = next_current
    # print(f"a: {area}, p: {corners}")
    return area * corners
 
assert(count_corners_in_neighbourhood([['O','O','O'], ['O','X','O'], ['O','O','O']]) == 4)
assert(count_corners_in_neighbourhood([['X','X','X'], ['X','X','X'], ['X','X','X']]) == 0)
assert(count_corners_in_neighbourhood([['X','O','X'], ['X','X','O'], ['X','X','X']]) == 1)
assert(count_corners_in_neighbourhood([['X','O','O'], ['X','X','O'], ['X','X','X']]) == 1)
assert(count_corners_in_neighbourhood([['X','O','X'], ['O','X','O'], ['X','X','X']]) == 2)
assert(count_corners_in_neighbourhood([['O','O','O'], ['O','X','O'], ['X','X','X']]) == 2)

visited = set()
answer1 = 0
for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        if (x,y) in visited:
            continue
        visited.add((x, y))
        answer1 += find_area_and_permimeter(grid, (x, y), visited)

visited = set()
answer2 = 0
for y in range(0, len(grid)):
    for x in range(0, len(grid[y])):
        if (x,y) in visited:
            continue
        visited.add((x, y))
        answer2 += find_area_and_edges(grid, (x, y), visited)

print(answer1)
print(answer2)
