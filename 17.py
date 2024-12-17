#!/usr/bin/env python
import re

CASE = 2

match CASE:
    case 0:
        input_file = 'input17_test_case_1.txt'
    case 1:
        input_file = 'input17_test_case_2.txt'        
    case 2:
        input_file = 'input17.txt'        
    case _:
        raise Exception("Unknown case")

with open(input_file, 'r') as f:
    register_prog = re.compile(r"Register ([ABC]): (\d+)")
    it = iter(f.readlines())
    
    m = register_prog.match(next(it))
    assert(m.group(1) == "A")
    rega = int(m.group(2))

    m = register_prog.match(next(it))
    assert(m.group(1) == "B")
    regb = int(m.group(2))

    m = register_prog.match(next(it))
    assert(m.group(1) == "C")
    regc = int(m.group(2))

    print(next(it))
    program = [int(ch) for ch in next(it).split("Program: ")[1].split(",")]

class Computer:

    def __init__(self, program, rega, regb, regc):
        self.program = program
        self.rega = rega
        self.regb = regb
        self.regc = regc
        self.pc = 0

    def combo(self, operand):
        if operand <= 3:
            return operand
        match operand:
            case 4:
                return self.rega
            case 5:
                return self.regb
            case 6:
                return self.regc
            case _:
                raise Exception("Unknown operand")

    def match_output(self, output_to_match):
        output = []
        while self.pc < len(self.program):
            opcode, operand = self.program[self.pc:self.pc + 2]
            match opcode:
                case 0: #adv, combo
                    self.rega = int(self.rega / 2 ** self.combo(operand))
                    self.pc += 2
                case 6: #bdv, combo
                    self.regb = int(self.rega / 2 ** self.combo(operand))
                    self.pc += 2
                case 7: #cdv, combo
                    self.regc = int(self.rega / 2 ** self.combo(operand))
                    self.pc += 2
                case 1: #bxl
                    self.regb = self.regb ^ operand
                    self.pc += 2
                case 4: #bxc
                    self.regb = self.regb ^ self.regc                
                    self.pc += 2
                case 2: #bst, combo
                    self.regb = self.combo(operand) % 8
                    self.pc += 2
                case 3: #jnz
                    if self.rega == 0:
                        self.pc += 2
                    else:
                        self.pc = operand
                case 5: #out, combo
                    new_output = self.combo(operand) % 8
                    if new_output != output_to_match[len(output)]:
                        return None
                    output.append(new_output)
                    self.pc += 2
        
        return output

    def run(self):
        output = []
        while self.pc < len(self.program):
            opcode, operand = self.program[self.pc:self.pc + 2]
            match opcode:
                case 0: #adv, combo
                    operand = self.combo(operand)
                    self.rega = int(self.rega / 2 ** operand)
                    self.pc += 2
                case 6: #bdv, combo
                    operand = self.combo(operand)
                    self.regb = int(self.rega / 2 ** operand)
                    self.pc += 2
                case 7: #cdv, combo
                    operand = self.combo(operand)
                    self.regc = int(self.rega / 2 ** operand)
                    self.pc += 2
                case 1: #bxl
                    self.regb = self.regb ^ operand
                    self.pc += 2
                case 4: #bxc
                    self.regb = self.regb ^ self.regc                
                    self.pc += 2
                case 2: #bst, combo
                    self.regb = self.combo(operand) % 8
                    self.pc += 2
                case 3: #jnz
                    if self.rega == 0:
                        self.pc += 2
                    else:
                        # print(f"Jump to {operand}")
                        self.pc = operand
                case 5: #out, combo
                    new_output = self.combo(operand) % 8
                    output.append(new_output)
                    self.pc += 2
        
        return output

###### TEST CASES ######
test_computer = Computer([2,6], 0, 0, 9)
test_output = test_computer.run()
assert(test_computer.regb == 1)

test_computer = Computer([5,0,5,1,5,4], 10, 0, 0)
test_output = test_computer.run()
assert(test_output == [0,1,2])

test_computer = Computer([0,1,5,4,3,0], 2024, 0, 0)
test_output = test_computer.run()
assert(test_computer.rega == 0)
assert(test_output == [4,2,5,6,7,7,7,7,3,1,0])

test_computer = Computer([1,7], 0, 29, 0)
test_output = test_computer.run()
assert(test_computer.regb == 26)

test_computer = Computer([4,0], 0, 2024, 43690)
test_output = test_computer.run()
assert(test_computer.regb == 44354)
###### END TEST CASES ######

print(f"Input: {program}, {rega}, {regb}, {regc}")
output = [str(i) for i in Computer(program, rega, regb, regc).run()]
print("Part 1: "+ ",".join(output))

# The only way to solve this is to figure out what the progmram acutally does. When you do
# you realise you can backtrack the solution and find the answer in chunks of 3 bits. 
a_possibilities = [(len(program) - 1, 0)]
a_definites = []
while a_possibilities:
    # print(a_possibilities)
    new_possibilities = []
    for index, apos in a_possibilities:
        for i in range(0, 8):
            apos_temp = (apos << 3) | i
            # print(bin(apos_temp))
            output = Computer(program, apos_temp, 0, 0).run()
            if output == program[index:]:
                if index == 0:
                    a_definites.append(apos_temp)
                    break
                new_possibilities.append((index - 1, apos_temp))

    a_possibilities = new_possibilities

# print(Computer(program, a, 0, 0).run())
print(f"Parr 2: {min(a_definites)}")

     


    
# while 1:
#     # if reg % 100000 == 0:
#     #     print(f"Reg: {reg}")
#     output = Computer(program, reg, 0, 0).match_output(program)
#     if output == program:
#         print(f"Rega: {reg}")
#         break
#     reg += 1

