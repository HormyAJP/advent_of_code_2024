def find_all_xmas(word_search):
    """Counts the total occurrences of the word "XMAS" in a word search.

    Args:
        word_search: A list of strings representing the rows of the word search.

    Returns:
        The total number of occurrences of the word "XMAS".
    """

    rows, cols = len(word_search), len(word_search[0])
    count = 0

    # Check horizontally
    for row in word_search:
        for col in range(cols - 3):
            if row[col:col+4] == "XMAS" or row[col:col+4] == "SXAM":
                count += 1

    # Check vertically
    for col in range(cols):
        for row in range(rows - 3):
            if word_search[row][col:col+4] == "XMAS" or word_search[row][col:col+4] == "SXAM":
                count += 1

    # Check diagonally (top-left to bottom-right)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if word_search[row][col:col+4] == "XMAS" or word_search[row][col:col+4] == "SXAM":
                count += 1

    # Check diagonally (bottom-left to top-right)
    for row in range(3, rows):
        for col in range(cols - 3):
            if word_search[row][col:col+4] == "XMAS" or word_search[row][col:col+4] == "SXAM":
                count += 1

    return count

# Read the input data from the file
with open('input4.txt', 'r') as f:
    word_search = [line.strip() for line in f]

# Count and print the number of occurrences of XMAS
total_xmas = find_all_xmas(word_search)
print(total_xmas)