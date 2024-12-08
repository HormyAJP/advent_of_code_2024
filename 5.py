# Gemini gave all the code below. The first version of is_valid_order didn't work.
# I just told it that "is_valid_order doesn't work correctly" and it gave me another.
# The second version of is_valid_order didn't work. I just said "Nope, still incorrect"
# The third version was correct.
# I was just blindly validating with the test case.

from collections import deque
from functools import cmp_to_key, partial
import copy


def is_valid_order(pages, rules):
    """Checks if the given page order is valid according to the rules.

    Args:
        pages: A list of page numbers.
        rules: A list of tuples (X, Y) representing the rules.

    Returns:
        True if the order is valid, False otherwise.
    """

    for i in range(len(pages) - 1):
        for rule in rules:
            if pages[i] == rule[0] and pages[i + 1] == rule[1]:
                return False
    return True

def is_valid_order(pages, rules):
    """Checks if the given page order is valid according to the rules.

    Args:
        pages: A list of page numbers.
        rules: A list of tuples (X, Y) representing the rules.

    Returns:
        True if the order is valid, False otherwise.
    """

    for i in range(len(pages) - 1):
        for j in range(i + 1, len(pages)):
            if (pages[i], pages[j]) in rules:
                return False
    return True

def is_valid_order(pages, rules):
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            if (pages[j], pages[i]) in rules:
                return False
    return True



def find_middle_page(pages):
    """Finds the middle page number in a list of pages.

    Args:
        pages: A list of page numbers.

    Returns:
        The middle page number.
    """

    return pages[len(pages) // 2]

def find_middle_page(pages):
    """Finds the middle page number or handles empty lists.

    Args:
        pages: A list of page numbers.

    Returns:
        The middle page number or 0 if the list is empty.
    """

    if not pages:
        return 0
    return pages[len(pages) // 2]


def solve(rules, updates):
    """Solves the problem by checking the validity of updates and summing middle page numbers.

    Args:
        rules: A list of tuples (X, Y) representing the rules.
        updates: A list of lists of page numbers.

    Returns:
        The sum of middle page numbers of valid updates.
    """

    total = 0
    for update in updates:
        if is_valid_order(update, rules):
            total += find_middle_page(update)
    return total



# Read the input data
with open('input5.txt', 'r') as f:
    rules_str, updates_str = f.read().split('\n\n')

# Parse rules and updates
rules = [tuple(map(int, line.split('|'))) for line in rules_str.splitlines()]
updates = [[int(num) for num in line.split(',')] for line in updates_str.splitlines()]

# Solve the problem and print the result
result = solve(rules, updates)
print(result)

bad_updates = []
for update in updates:
    if not is_valid_order(update, rules):
        bad_updates.append(update)

def compare_with_rules(rules, a, b):
    for rule in rules:
        if a == rule[0] and b == rule[1]:
            return -1
        if a == rule[1] and b == rule[0]:
            return 1
    # I tried to overcomplicate this initially. I wasn't clear that all
    # relationships would be explicit. I thought that I'd have to 
    # infer some through transitivity, e.g. A|B and B|C => A|C.
    # Turns out not :shrug:
    raise Exception("SHIT")
            
def reorder_bad_update(update, rules):
    compare = partial(compare_with_rules, rules)
    update = sorted(update, key=cmp_to_key(compare))
    return update


total = 0
for bad_update in bad_updates:
    update = reorder_bad_update(bad_update, rules)
    print(f"{bad_update} => {update}")
    total += find_middle_page(update)
print(total)