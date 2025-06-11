#!/usr/bin/env python

import numpy as np

CASE = 1
match CASE:
    case 0:
        input_file = 'input25_test_case_1.txt'
    case 1:
        input_file = 'input25.txt'        
    case _:
        raise Exception("Unknown case")


class LockOrKey:
    def __init__(self, nparray, islock):
        self.nparray = nparray
        self.islock = islock
        self._process_heights()

    def _process_heights(self):
        self.heights = []
        # count the number of hashes in each column
        for i in range(0, 5):
            unique, counts = np.unique(self.nparray[:,i], return_counts=True)
            d = dict(zip(unique, counts))
            if '#' not in d:
                self.heights.append(0)
            else:
                self.heights.append(d['#'])
    
    def __str__(self):
        return str(self.nparray)
    
    def __repr__(self):
        return str(self)

keys = []
locks = []
with open(input_file, 'r') as f:
    it = iter(f.readlines())
    try:
        while 1:
            first_line = next(it).strip()
            new = []
            islock = False
            if set(first_line) == {"#"}:
                islock = True
                for i in range(0, 6):
                    new.append(list(next(it).strip()))                
            elif set(first_line.strip()) == {"."}:
                islock = False
                new.append(list(first_line))
                for i in range(0, 5):
                    new.append(list(next(it).strip()))                                
                next(it)
            else:
                assert(False)
            
            new = np.array(new).reshape(6, 5)

            if islock:
                locks.append(LockOrKey(new, islock))
            else:
                keys.append(LockOrKey(new, islock))
            next(it)
    except StopIteration:
        pass

matches = []
for key in keys:
    for lock in locks:
        match = True
        for i in range(0, 5):
            if key.heights[i] + lock.heights[i] > 5:
                match = False
                break
        if match:
            matches.append((key, lock))

print(len(matches))















