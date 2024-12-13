#!/usr/bin/env python

import math
import sys
import numpy as np
import re

class Machine:

    def __init__(self, a, b, prize):
        self.a = a
        self.b = b
        self.prize = prize

    def __str__(self):
        return f"Machine({self.a}, {self.b}, {self.prize})"
        # return f"{self.a[0]}x + {self.b[0]}y = {self.prize[0]}\n{self.a[1]}x + {self.b[1]}y = {self.prize[1]}"

with open('input13.txt', 'r') as f:
    machines = []
    button_prog = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)\n")
    prize_prog = re.compile(r"Prize: X=(\d+), Y=(\d+)\n")
    iterator = iter(f.readlines())
    try:
        while 1:
            m = button_prog.match(next(iterator))
            if not m:
                raise Exception("Button A not found")
            a = (int(m.group(1)), int(m.group(2)))
            m = button_prog.match(next(iterator))
            if not m:
                raise Exception("Button B not found")
            b = (int(m.group(1)), int(m.group(2)))
            m = prize_prog.match(next(iterator))
            if not m:
                raise Exception("Prize not found")
            next(iterator) # Skip empty line
            prize = (int(m.group(1)), int(m.group(2)))
            machines.append(Machine(a, b, prize))
    except StopIteration as ex:
        # Code is crappy. Expects two blank lines at the end of the file
        pass

# assert(len(machines)==320)

def is_zero(num, tolerance=1e-5):
    if abs(num) < tolerance:
        return True
    return False

def is_non_negative_integer(num, tolerance=1e-5):
    if num < 0:
        return False
    # print(abs(num - round(num)))
    if abs(num - round(num)) < tolerance:
        return True
    return False

def check(presses, a, b, prize, tolerance=1e-5):
    presses = presses.flatten().tolist()
    result = (presses[0] * a[0] + presses[1] * b[0], presses[0] * a[1] + presses[1] * b[1])
    print(f"Comparing {result} to {prize}")
    return is_zero(result[0] - prize[0], tolerance) and is_zero(result[1] - prize[1], tolerance)

spend = 0
for m in machines:
    # print(m)

    # Check for linear dependence
    if is_zero(m.a[0]/m.b[0] * m.b[1] - m.a[1]):
        print(m)
        raise Exception("Rejecting due to linear dependence")

    matrix = np.array([[m.a[0], m.b[0]], [m.a[1], m.b[1]]])
    inverse_matrix = np.linalg.inv(matrix)
    prize = column_vector = np.array(m.prize).reshape(-1, 1)
    res = np.dot(inverse_matrix, prize)
    
    assert(check(res, m.a, m.b, m.prize))

    if is_non_negative_integer(res.item(0)) and is_non_negative_integer(res.item(1)):
        # print(f"Accepting {res.item(0)}, {res.item(1)}")
        assert(res.item(0) <= 100)
        assert(res.item(1) <= 100)
        spend += round(res.item(0)) * 3 + round(res.item(1))
    else:
        # print(f"Rejecting {res[0]}, {res[1]}")
        pass
    
print(spend)

spend = 0
for m in machines:
    # print(m)

    m.prize = (m.prize[0] + 10000000000000, m.prize[1] + 10000000000000)
    # Check for linear dependence
    if is_zero(m.a[0]/m.b[0] * m.b[1] - m.a[1]):
        print(m)
        raise Exception("Rejecting due to linear dependence")

    matrix = np.array([[m.a[0], m.b[0]], [m.a[1], m.b[1]]])
    inverse_matrix = np.linalg.inv(matrix)
    prize = column_vector = np.array(m.prize).reshape(-1, 1)
    res = np.dot(inverse_matrix, prize)

    if is_non_negative_integer(res.item(0), tolerance=1e-4) and is_non_negative_integer(res.item(1), tolerance=1e-4):
        # print(f"Accepting {res.item(0)}, {res.item(1)}")
        spend += round(res.item(0)) * 3 + round(res.item(1))
    else:
        # print(f"Rejecting {res[0]}, {res[1]}")
        pass
    
print(spend)
