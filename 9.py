#!/usr/bin/env python

with open('input9.txt', 'r') as f:
    input = [int(ch) for ch in f.read()]

def expand_input(input):
    expanded = []
    file_id = 0
    for i in range(0, len(input), 2):
        expanded += [str(file_id)] * input[i]
        file_id+=1
        if i + 1 < len(input):
            expanded += ["."] * input[i+1]
    return expanded

# assert(expand_input(input) == [ch for ch in "00...111...2...333.44.5555.6666.777.888899"])

def find_next_free(expanded, start):
    for i in range(start, len(expanded)):
        if expanded[i] == ".":
            return i
    return -1

def find_last_block(expanded, start):
    while start >= 0:
        if expanded[start] != ".":
            return start
        start -= 1
    raise Exception("No block found")

def defrag(expanded):
    next_free = find_next_free(expanded, 0)
    last_block = find_last_block(expanded, len(expanded) - 1)
    while next_free != -1 and next_free < last_block:
        expanded[next_free], expanded[last_block] = expanded[last_block], expanded[next_free]
        next_free = find_next_free(expanded, next_free)
        last_block = find_last_block(expanded, last_block)

expanded = expand_input(input)
# defrag(expanded)

def checksum(expanded):
    sum = 0
    for i in range(0, len(expanded)):
        if expanded[i] == ".":
            continue
        sum += i * int(expanded[i])
    return sum

# print(checksum(expanded))

# assert(expanded == [ch for ch in "0099811188827773336446555566.............."])

def find_free_block_of_size(expanded, size):
    i = 0
    while i < len(expanded):
        if expanded[i] != ".":
            i += 1
            continue
        count = 0
        while count < size and i + count < len(expanded) and expanded[i + count] == "." :
            count += 1
        if count == size:
            return i
        i += count
    return -1
        
def find_file_id(expanded, file_id, start):
    found = False
    while start >= 0:
        if found:
            if expanded[start] !=str(file_id):
                return start + 1
        else:
            if expanded[start] == str(file_id):
                found = True
        start -= 1
    if found:
        return 0
    raise Exception(f"File not found: {file_id}")

def length_of_file(expanded, start):
    file_id = expanded[start]
    size = 0
    while start + size < len(expanded) and expanded[start + size] == file_id:
        size += 1
    return size

def defrag2(expanded):
    i = len(expanded) - 1
    while expanded[i] == ".":
        i -= 1
        
    file_id = int(expanded[i])
    while file_id >= 0:
        print(file_id)
        file_index = find_file_id(expanded, file_id, len(expanded) - 1)
        file_len = length_of_file(expanded, file_index)
        free_index = find_free_block_of_size(expanded, file_len)
        if free_index == -1 or free_index > file_index:
            file_id -= 1
            continue
        for i in range(0, file_len):            
            expanded[free_index + i] = str(file_id)
            expanded[file_index + i] = "."
        file_id -= 1

#### TEST CASES ####
# test_expanded = "00992111777.44.333....5555.6666.....8888.."
# index = find_file_id(test_expanded, 0, len(test_expanded) - 1)
# assert(length_of_file(test_expanded, index) == 2)
# index = find_file_id(test_expanded, 1, len(test_expanded) - 1)
# assert(length_of_file(test_expanded, index) == 3)
# index = find_file_id(test_expanded, 2, len(test_expanded) - 1)
# assert(length_of_file(test_expanded, index) == 1)
# index = find_file_id(test_expanded, 3, len(test_expanded) - 1)
# assert(length_of_file(test_expanded, index) == 3)
# index = find_file_id(test_expanded, 8, len(test_expanded) - 1)
# assert(length_of_file(test_expanded, index) == 4)

# assert(find_free_block_of_size(test_expanded, 1) == 11)
# assert(find_free_block_of_size(test_expanded, 2) == 18)
# assert(find_free_block_of_size(test_expanded, 3) == 18)
# assert(find_free_block_of_size(test_expanded, 4) == 18)
# assert(find_free_block_of_size(test_expanded, 5) == 31)

#### END TEST CASES ####

defrag2(expanded)
print(checksum(expanded))

# assert(expanded == [ch for ch in "00992111777.44.333....5555.6666.....8888.."])