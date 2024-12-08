#!/usr/bin/env python

import copy
from enum import Enum
import itertools
class Operator(Enum):
    Add = "+"
    Multiply = "*"
    Concatenate = "|"

def log(msg):
    # print(msg)
    pass

# Read the input from a file
with open('input7.txt', 'r') as f:
    input_data = []
    for line in f:
        sum, values = line.split(':')
        values = [int(v) for v in values.split()]
        input_data.append([int(sum)] + values)

def sum_check(target, values, use_concatenate=False):
    if use_concatenate:
        operators = [Operator.Add, Operator.Multiply, Operator.Concatenate]
    else:
        operators = [Operator.Add, Operator.Multiply]
    log(f"====================")
    log(f"Checking: {sum} and {values}")
    for operator_combo in itertools.product(operators, repeat=len(values) - 1):
        log(f"Using operators: {[op.value for op in operator_combo]}")
        mutated_values = copy.copy(values)
        for i in range(len(operator_combo)):
            match operator_combo[i]:
                case Operator.Add:
                    log(f"{mutated_values[i]} + {mutated_values[i+1]}")
                    mutated_values[i+1] = mutated_values[i] + mutated_values[i+1]
                case Operator.Multiply:
                    log(f"{mutated_values[i]} * {mutated_values[i+1]}")
                    mutated_values[i+1] = mutated_values[i] * mutated_values[i+1]
                case Operator.Concatenate:
                    log(f"{mutated_values[i]} | {mutated_values[i+1]}")
                    mutated_values[i+1] = int(str(mutated_values[i]) + str(mutated_values[i+1]))
            log(f"Mutated values: {mutated_values}")
            if mutated_values[i+1] > target:
                log(f"Failed: {mutated_values[i+1]} > {target}")
                mutated_values[-1] = target - 1
                break
        if mutated_values[-1] == target:
            log("Success")
            return True
        else:
            log(f"Failed: {mutated_values[-1]} != {target}")
            pass
    return False

answer1 = 0
for data in input_data:
    if sum_check(data[0], data[1:]):
        answer1 += data[0]
print(answer1)

answer2 = 0
for data in input_data:
    if sum_check(data[0], data[1:], use_concatenate=True):
        answer2 += data[0]
print(answer2)
