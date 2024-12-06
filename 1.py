# This was fully AI generated

def calculate_distance(left_list, right_list):
  """Calculates the total distance between two lists of numbers.

  Args:
    left_list: A list of numbers.
    right_list: A list of numbers.

  Returns:
    The total distance between the two lists.
  """

  left_list.sort()
  right_list.sort()

  total_distance = 0
  for left, right in zip(left_list, right_list):
    total_distance += abs(left - right)

  return total_distance

left_list=[]
right_list=[]
with open('input1.txt', 'r') as f:
  for line in f:
    lnum, rnum = line.split()
    left_list.append(int(lnum))
    right_list.append(int(rnum))

# Calculate and print the total distance
total_distance = calculate_distance(left_list, right_list)
print(total_distance)

def calculate_similarity_score(left_list, right_list):
  """Calculates the similarity score between two lists of numbers.

  Args:
    left_list: A list of numbers.
    right_list: A list of numbers.

  Returns:
    The similarity score between the two lists.
  """

  # Create a dictionary to count the frequency of numbers in the right list
  right_counts = {}
  for num in right_list:
    right_counts[num] = right_counts.get(num, 0) + 1

  similarity_score = 0
  for num in left_list:
    similarity_score += num * right_counts.get(num, 0)

  return similarity_score


# Calculate and print the similarity score
similarity_score = calculate_similarity_score(left_list, right_list)
print(similarity_score)