#!/usr/bin/env python

import collections
import functools
import sys
import time

CASE = 1
match CASE:
    case 0:
        input_file = 'input22_test_case_1.txt'
    case 1:
        input_file = 'input22.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    initial_secret_numbers = [int(line.strip()) for line in f.readlines()]

@functools.lru_cache(maxsize=None)
def evolve(number):
    number = (number ^ (number << 6)) & 0b0111111111111111111111111
    number = (number ^ (number >> 5)) 
    return (number ^ (number << 11)) & 0b0111111111111111111111111

#### TESTS ####
test_evolutions = [
    123,
    15887950,
    16495136,
    527345,
    704524,
    1553684,
    12683156,
    11100544,
    12249484,
    7753432,
    5908254,
]

for inumber in range(len(test_evolutions) - 1):
    assert(evolve(test_evolutions[inumber]) == test_evolutions[inumber + 1])

for inumber in range(len(test_evolutions) - 1):
    assert(evolve(test_evolutions[inumber]) % 10 == test_evolutions[inumber + 1] % 10)

#### TESTS ####

all_diffs = set()

for i in range(0, 10):
    start = time.time()
    answer1 = 0
    evolve_cache = {}
    for number in initial_secret_numbers:
        initial_number = number
        evolve_cache[initial_number] = []
        current_diff = collections.deque(maxlen=4)

        for i in range(0, 3):
            previous = number
            number = evolve(previous)    
            evolve_cache[initial_number].append(number)         
            current_diff.append(number % 10 - previous % 10)

        for i in range(3, 2000):    
            previous = number
            number = evolve(previous)  
            evolve_cache[initial_number].append(number)  
            current_diff.append(number % 10 - previous % 10)
            all_diffs.add(tuple(current_diff))

        answer1 += number
    end = time.time()
    print(f"Time: {end - start}")
    print(f"Part 1: {answer1}")    

# for i in range(0, 10):
#     start = time.time()
#     answer1 = 0
#     for number in initial_secret_numbers:
#         initial_number = number
#         current_diff = collections.deque(maxlen=4)

#         for i in range(0, 3):
#             previous = number
#             number = evolve(previous)    
#             current_diff.append(number % 10 - previous % 10)

#         for i in range(3, 2000):    
#             previous = number
#             number = evolve(previous)  
#             current_diff.append(number % 10 - previous % 10)

#         answer1 += number
#     end = time.time()
#     print(f"Time: {end - start}")
#     # print(f"Part 1: {answer1}")  

best_bananas = 0
best_banana_diff = None
for diff in all_diffs:
    start = time.time()    
    total_bananas = 0
    for number in initial_secret_numbers:
        current_diff = collections.deque(maxlen=4)
        it = iter(evolve_cache[number])
        for i in range(0, 3):
            previous = number            
            number = next(it)      
            current_diff.append(number % 10 - previous % 10)        

        try:
            while 1:
                previous = number            
                number = next(it)
                current_diff.append(number % 10 - previous % 10)
                # if tuple(current_diff) == diff:
                #     total_bananas += 1
                #     break
        except StopIteration:
            pass
    if total_bananas > best_bananas:
        best_bananas = total_bananas
        best_banana_diff = diff
    end = time.time()
    print(f"Time: {end - start}")        

print(f"Part 2: {best_bananas}, {best_banana_diff}")    

