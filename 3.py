import re

def parse_mul_instructions(input_str):
  """Parses a string containing mul instructions and returns the sum of their results.

  Args:
    input_str: The input string containing mul instructions.

  Returns:
    The sum of the results of all valid mul instructions.
  """

  pattern = r"mul\((\d+),(\d+)\)"
  matches = re.findall(pattern, input_str)

  total = 0
  for match in matches:
    num1, num2 = int(match[0]), int(match[1])
    total += num1 * num2

  return total

# Read the input data from the file
with open('input3.txt', 'r') as f:
  input_str = f.read()

# Parse the instructions and print the total
total_result = parse_mul_instructions(input_str)
print(total_result)

import re

def parse_mul_instructions_with_conditionals(input_str):
  """Parses a string containing mul instructions with do/don't conditionals and returns the sum of their results.

  Args:
    input_str: The input string containing mul instructions and conditionals.

  Returns:
    The sum of the results of all enabled mul instructions.
  """

  pattern = r"(do\(\)|don't\(\))|mul\((\d+),(\d+)\)"
  total = 0
  enabled = True

  for match in re.finditer(pattern, input_str):
    if match.group(1) == "do()":
      enabled = True
    elif match.group(1) == "don't()":
      enabled = False
    else:
      if enabled:
        num1, num2 = int(match.group(2)), int(match.group(3))
        total += num1 * num2

  return total

# Read the input data from the file
with open('input3.txt', 'r') as f:
  input_str = f.read()

# Parse the instructions and print the total
total_result = parse_mul_instructions_with_conditionals(input_str)
print(total_result)