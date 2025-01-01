#!/usr/bin/env python

import itertools
import sys

CASE = 0
match CASE:
    case 0:
        input_file = 'input21_test_case_1.txt'
    case 1:
        input_file = 'input21.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    keycodes = [line.strip() for line in f.readlines()]

def assert_equals(a, b):
    if a != b:
        print(f"{a} != {b}")
        assert(False)

class X_Ception(Exception):
    pass    

class Robot:

    def __init__(self, grid):
        self.grid = grid
        self.reset()

    def reset(self):
        self.position = self.find_key_in_grid("A")

    def find_key_in_grid(self, key):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == key:
                    return (x, y)
        raise Exception(f"Key {key} not found")
    
    def move(self, key):
        movements = []
        key_position = self.find_key_in_grid(key)
        xmove = key_position[0] - self.position[0] 
        ymove = key_position[1] - self.position[1]
        if ymove < 0:
            movements += ["^"] * abs(ymove)
        if xmove > 0:
            movements += [">"] * xmove
        if ymove > 0:
            movements += ["v"] * ymove            
        if xmove < 0:
            movements += ["<"] * abs(xmove)            
        movements.append("A")
        self.position = key_position
        return movements

    def filter_x_hites(self, movements):
        cached_key_position = self.position
        filtered_movements = []
        for movement in movements:
            self.reset()
            try:
                self.run_instructions(movement, reject_x=True)
                filtered_movements.append(movement)
            except X_Ception:
                pass
        self.position = cached_key_position
        return filtered_movements

    def move_combinations(self, key):
        movements = []
        key_position = self.find_key_in_grid(key)
        xmove = key_position[0] - self.position[0] 
        ymove = key_position[1] - self.position[1]
        if ymove < 0:
            movements += ["^"] * abs(ymove)
        if xmove > 0:
            movements += [">"] * xmove
        if ymove > 0:
            movements += ["v"] * ymove            
        if xmove < 0:
            movements += ["<"] * abs(xmove)            
        
        self.position = key_position

        unique_permutations = set()
        for permutation in itertools.permutations(movements):
            unique_permutations.add(permutation)
        return self.filter_x_hites([list(p) + ["A"] for p in unique_permutations])

    def instructions_for_robot_combinations(self, keycode):
        self.reset()
        movements = []
        for key in keycode:
            movements.append(self.move_combinations(key))
        return movements

    def instructions_for_robot(self, keycode):
        self.reset()
        movements = []
        for key in keycode:
            movements += self.move(key)
        return "".join(movements)
    
    def run_instructions(self, instructions, reject_x=False):
        self.reset()
        output = []
        for instruction in instructions:
            match instruction:
                case "v":
                    self.position = (self.position[0], self.position[1] + 1)
                case "^":
                    self.position = (self.position[0], self.position[1] - 1)
                case ">":
                    self.position = (self.position[0] + 1, self.position[1])
                case "<":
                    self.position = (self.position[0] - 1, self.position[1])
                case "A":
                    output.append(self.grid[self.position[1]][self.position[0]])
            if reject_x and self.grid[self.position[1]][self.position[0]] == "X":
                raise X_Ception()
        return "".join(output)

def line_up_As(bigger, smaller):
    extended_smaller = ""
    j = 0
    for i in range(0, len(bigger)):
        if bigger[i] == "A":
            extended_smaller += smaller[j]
            j += 1
        else:
            extended_smaller += " "
    return extended_smaller

def numeric_part_of_keycode(keycode):
    return int(keycode.replace('A', ''))

keypad_robot = Robot([
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["X", "0", "A"],
])

direction_robot = Robot([
    ["X", "^", "A"],
    ["<", "v", ">"],
])

direction_robot.reset()
assert(set(["".join(l) for l in direction_robot.move_combinations("<")]) == {"<v<A", "v<<A"})
direction_robot.reset()
assert(set(["".join(l) for l in direction_robot.move_combinations("A")]) == {"A"})
direction_robot.reset()
assert(set(["".join(l) for l in direction_robot.move_combinations("v")]) == {"<vA", "v<A"})
direction_robot.reset()
assert(set(["".join(l) for l in direction_robot.move_combinations(">")]) == {"vA"})
keypad_robot.reset()
assert_equals(set(["".join(l) for l in keypad_robot.move_combinations("4")]), {"^^<<A", "^<^<A", "<^^<A", "<^<^A", "^<<^A"})

def run_to_end(instructions, num_robots, space_out=False):
    all_run = run_direction_robots_n_times(instructions, num_robots, space_out)
    ins = all_run[-1].replace(" ", "")
    final_code = keypad_robot.run_instructions(ins)
    return all_run + [final_code]

def run_direction_robots_n_times(instructions, num_robots, space_out=False):
    all_run = [instructions]
    all_run_spaced = [instructions]
    for _ in range(0, num_robots):
        all_run.append(direction_robot.run_instructions(all_run[-1]))
        all_run_spaced.append(line_up_As(all_run_spaced[-1], all_run[-1]))    
    if space_out:
        return all_run_spaced
    else:
        return all_run
    
# total_complexity = 0
# for keycode in keycodes:
#     print(f"Keycode: {keycode}")
#     ins1 = keypad_robot.instructions_for_robot(keycode)
#     print(ins1)
#     assert(keypad_robot.run_instructions(ins1) == keycode)
#     ins2 = direction_robot.instructions_for_robot(ins1)
#     print(ins2)
#     assert(direction_robot.run_instructions(ins2) == ins1)
#     ins3 = direction_robot.instructions_for_robot(ins2)
#     print(ins3)
#     assert(direction_robot.run_instructions(ins3) == ins2)

#     print(f"Complexity for {keycode} is {len(ins3)} * {numeric_part_of_keycode(keycode)} = {len(ins3) * numeric_part_of_keycode(keycode)}")
#     total_complexity += len(ins3) * numeric_part_of_keycode(keycode)

def flatten(xss):
    return [x for xs in xss for x in xs]

def iterate_direction_robots(instructions, depth):
    '''Returns a pair with the first element being the minimum number of instructions
    and the second element being the instructions that achieve that minimum'''
    if depth == 0:
        return [len(instructions), instructions]
    
    # steps will be an array of arrays. Each element of the top most array is 
    # a step we can calculate indepenedently. Each element of the nested arrays
    # is a way of achieving that step.
    steps = direction_robot.instructions_for_robot_combinations(instructions)
    
    instruction_count_minima = [sys.maxsize] * len(steps)
    instruction_minima = [None] * len(steps)

    for istep, step in enumerate(steps):
        for instructions in step:
            count, ins = iterate_direction_robots(instructions, depth - 1)
            if count < instruction_count_minima[istep]:
                instruction_count_minima[istep] = count
                instruction_minima[istep] = ins

    
    return [sum(instruction_count_minima), "".join(flatten(instruction_minima))]


def optimize_keycode(keycode, num_direction_robots):
    # steps will be an array of arrays. Each element of the top most array is 
    # a step we can calculate indepenedently. Each element of the nested arrays
    # is a way of achieving that step.    
    steps = keypad_robot.instructions_for_robot_combinations(keycode)
    
    instruction_count_minima = [sys.maxsize] * len(steps)
    instruction_minima = [None] * len(steps)

    for istep, step in enumerate(steps):
        for instructions in step:
            count, ins = iterate_direction_robots(instructions, num_direction_robots)
            if count < instruction_count_minima[istep]:
                instruction_count_minima[istep] = count
                instruction_minima[istep] = ins
    
    return [sum(instruction_count_minima), "".join(flatten(instruction_minima))]


########## TESTS #########
test_instrucions = "<<A>^A>A"
assert(iterate_direction_robots(test_instrucions, 0)[0] == len(test_instrucions))
for i in range(1, 5):
    final_instructions = iterate_direction_robots(test_instrucions, i)[1]
    assert_equals(run_direction_robots_n_times(final_instructions, i, False)[-1], test_instrucions)



x3 = optimize_keycode("179A", 2)[1]
print(x3)
x2 = direction_robot.run_instructions(x3)
x2l = line_up_As(x3, x2)
print(x2l)
x1 = direction_robot.run_instructions(x2)
print(line_up_As(x2l, x1))
x = keypad_robot.run_instructions(x1)
print(x)

#v<A<AA^>>AA<A>vA^AvA^Av<<A^>>AAvA^Av<A^>AA<A>Av<A<A^>>AAA<A>vA^A
#<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A



test_minimum, test_instructions = optimize_keycode("029A", 2)
assert_equals(test_minimum, 68)
assert_equals(run_to_end(test_instructions, 2)[-1], "029A")
assert_equals(optimize_keycode("980A", 2)[0], 60)
test_minimum, test_instructions = optimize_keycode("179A", 2)
all = run_to_end(test_instructions, 2, space_out=True)
for x in all:
    print(x)

assert_equals(optimize_keycode("179A", 2)[0], 68)
assert_equals(optimize_keycode("456A", 2)[0], 64)
assert_equals(optimize_keycode("379A", 2)[0], 64)

total_complexity = 0
for keycode in keycodes:
    minsteps = optimize_keycode(keycode, num_direction_robots=2)
    complexity = minsteps * numeric_part_of_keycode(keycode)
    print(f"Optimized complexity for {keycode} is {minsteps} * {numeric_part_of_keycode(keycode)} = {complexity}")
    total_complexity += complexity

print(total_complexity)
