#!/usr/bin/env python

import sys
import graphviz
import re

wire_prog = re.compile(r"(.*): ([01])")
gate_prog = re.compile(r"(.*) ([A-Z]+) (.*) -> (.*)")

CASE = 2
match CASE:
    case 0:
        input_file = 'input24_test_case_1.txt'
    case 1:
        input_file = 'input24_test_case_2.txt'        
    case 2:
        input_file = 'input24.txt'        
    case _:
        raise Exception("Unknown case")

class Gate:

    def __init__(self, left, right, op, output):
        assert(op in ['AND', 'OR', 'XOR'])
        self.op = op
        self.left = left
        self.right = right
        self.output = output
        self.value = None

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.op == other.op and self.output == other.output

    def __str__(self):
        return f"{self.left} {self.op} {self.right} -> {self.output}"
    
    def __repr__(self):
        return str(self)
    
    def compute(self, lvalue, rvalue):
        if self.op == 'AND':
            return lvalue & rvalue
        elif self.op == 'OR':
            return lvalue | rvalue
        elif self.op == 'XOR':
            return lvalue ^ rvalue
        else:
            raise Exception("Unknown op")
    
    def from_string(input):
        m = gate_prog.match(input)
        if m:
            return Gate(m.group(1), m.group(3), m.group(2), m.group(4))
        else:
            raise Exception("Invalid input")

wires = {}
gates = []
with open(input_file, 'r') as f:
    for line in f.readlines():
        m = wire_prog.match(line.strip())
        if m:
            assert(m.group(1) not in wires)
            assert(m.group(2) in ['0', '1'])
            wires[m.group(1)] = int(m.group(2))
        m = gate_prog.match(line.strip())
        if m:
            assert(m.group(4) not in wires)
            output = m.group(4)
            assert(output not in wires)
            wires[output] = None
            gates.append(Gate(m.group(1), m.group(3), m.group(2), output))










# # swap1A = Gate('x06', 'y06', 'AND', 'z06')
# # swap1B = Gate('smt', 'chv',  'OR', 'cjt')
# # swap1A = Gate.from_string("cjt AND sfm -> fmd")
# # swap1B = Gate.from_string("cjt XOR sfm -> jmq")
# # for gate in gates:
# #     if gate == swap1A:
# #         gate.output = swap1B.output
# #     if gate == swap1B:
# #         gate.output = swap1A.output

# dot = graphviz.Digraph()

# zeds = set()
# with dot.subgraph(name='terminal_rank') as s:
#     for gate in gates:
#         dot.node(gate.output)
#         dot.edge(gate.left, gate.output)
#         dot.edge(gate.right, gate.output)
#         if gate.output.startswith("z"):
#             zeds.add(gate.output)
# l = list(zeds)
# l.sort()
# for i in range(0, len(l) - 1):
#     dot.edge(l[i], l[i + 1], style='invis')

# dot.render('24.gv', view=True)

# sys.exit(0)


def compute_all_outputs(gates, wires):
    while None not in wires.values():
        for gate in gates:
            if gate.value is not None:
                continue

            if gate.left in wires and gate.right in wires:
                gate.value = gate.compute(wires[gate.left], wires[gate.right])
                wires[gate.output] = gate.value
                gates.remove(gate)
                continue

all_z_keys = []
for key in wires.keys():
    if key.startswith("z"):
        all_z_keys.append(key)
all_z_keys.sort(reverse=True)

binary = "0b"
for key in all_z_keys:
    binary += str(wires[key])

print(int(binary, 2))




