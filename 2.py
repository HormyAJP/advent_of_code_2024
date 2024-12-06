def is_safe_with_dampener(report):
  """Checks if a report is safe, considering the Problem Dampener.

  Args:
    report: A list of numbers representing the levels in a report.

  Returns:
    True if the report is safe, False otherwise.
  """

  if is_safe_report(report):
    return True

  for i in range(len(report)):
    modified_report = report[:i] + report[i+1:]
    if is_safe_report(modified_report):
      return True

  return False


def is_safe_report(report):
  """Checks if a report is safe.

  Args:
    report: A list of numbers representing the levels in a report.

  Returns:
    True if the report is safe, False otherwise.
  """

  increasing = None  # None: undecided, True: increasing, False: decreasing
  for i in range(1, len(report)):
    diff = report[i] - report[i - 1]
    if diff == 0:
      return False
    if increasing is None:
      increasing = diff > 0
    elif increasing != (diff > 0):
      return False
    if abs(diff) > 3:
      return False
  return True

def count_safe_reports(reports):
  """Counts the number of safe reports in a list of reports.

  Args:
    reports: A list of lists of numbers, where each inner list represents a report.

  Returns:
    The number of safe reports.
  """

  safe_count = 0
  for report in reports:
    if is_safe_with_dampener(report):
      safe_count += 1
  return safe_count

# Read the input data from the file
with open('input2.txt', 'r') as f:
  reports = [[int(num) for num in line.split()] for line in f]

# Count and print the number of safe reports
safe_reports = count_safe_reports(reports)
print(safe_reports)

