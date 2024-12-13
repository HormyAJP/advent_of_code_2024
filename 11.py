#!/usr/bin/env python

with open('input11.txt', 'r') as f:
    input_numbers = [int(i) for i in f.read().strip().split()]

def compress(num_and_count):
    new_num_and_count = []
    seen_before = {}
    for pr in num_and_count:
        if pr[0] not in seen_before:
            seen_before[pr[0]] = pr[1]
        else:
            seen_before[pr[0]] += pr[1]
    for key, value in seen_before.items():
        new_num_and_count.append((key, value))
    return new_num_and_count

def evolve(num_and_count, blinks):
    for i in range(0, blinks):
        num_and_count = compress(num_and_count)
        new_num_and_count = []
        for pr in num_and_count:
            num_string = str(pr[0])
            if pr[0] == 0:
                new_num_and_count.append((1, pr[1]))
            elif len(num_string) % 2 == 0:
                halfway = int(len(num_string)/2)
                left = int(num_string[0:halfway])
                right = int(num_string[halfway:])
                new_num_and_count.append((left, pr[1]))
                new_num_and_count.append((right, pr[1]))
            else:
                new_num_and_count.append((pr[0] * 2024, pr[1]))       
        num_and_count = new_num_and_count
    return new_num_and_count

# We compress data into pairs where the first value is the actual number that would appear in the
# list and the second is the number of times that number would appear in the list.
# If we don't avoid repetitions then the list will become ubreasonably long.
num_and_count = [(n,1) for n in input_numbers]
num_and_count = evolve(num_and_count, blinks=75)

total = 0
for pr in num_and_count:
    total += pr[1]

print(total)
