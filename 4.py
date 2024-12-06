# Gemini on it's own failed. But with me writing the function and GH copilot completing, this worked.
def find_all_xmas(word_search):
    count = 0
    width = len(word_search[0])
    height = len(word_search)
    for col in range(len(word_search)):
        for row in range(len(word_search[col])):
            if word_search[row][col] != "X":
                continue
            # Go right
            if col + 3 < width:
                if word_search[row][col:col+4] == "XMAS":
                    count += 1
            # Go left
            if col - 3 >= 0:
                if word_search[row][col] + word_search[row][col-1] + word_search[row][col-2] + word_search[row][col-3] == "XMAS":
                    count += 1
            # Go up
            if row - 3 >= 0:
                if word_search[row][col] + word_search[row-1][col] + word_search[row-2][col] + word_search[row-3][col] == "XMAS":
                    count += 1
            # Go down
            if row + 3 < height:
                if word_search[row][col] + word_search[row+1][col] + word_search[row+2][col] + word_search[row+3][col] == "XMAS":
                    count += 1
            # Go up-right
            if row - 3 >= 0 and col + 3 < width:
                if word_search[row][col] + word_search[row-1][col+1] + word_search[row-2][col+2] + word_search[row-3][col+3] == "XMAS":
                    count += 1
            # Go up-left
            if row - 3 >= 0 and col - 3 >= 0:
                if word_search[row][col] + word_search[row-1][col-1] + word_search[row-2][col-2] + word_search[row-3][col-3] == "XMAS":
                    count += 1
            # Go down-right
            if row + 3 < height and col + 3 < width:
                if word_search[row][col] + word_search[row+1][col+1] + word_search[row+2][col+2] + word_search[row+3][col+3] == "XMAS":
                    count += 1  
            # Go down-left
            if row + 3 < height and col - 3 >= 0:
                if word_search[row][col] + word_search[row+1][col-1] + word_search[row+2][col-2] + word_search[row+3][col-3] == "XMAS":
                    count += 1

    return count

def find_all_mas_exes(word_search):        
    count = 0
    width = len(word_search[0])
    height = len(word_search)
    for col in range(1, width - 1):        
        for row in range(1, height - 1):
            if word_search[row][col] != "A":
                continue
            match word_search[row-1][col-1]:
                case "M":
                    if word_search[row+1][col+1] != "S":
                        continue
                case "S":
                    if word_search[row+1][col+1] != "M":
                        continue                    
                case _:
                    continue
            match word_search[row-1][col+1]:
                case "M":
                    if word_search[row+1][col-1] != "S":
                        continue
                case "S":
                    if word_search[row+1][col-1] != "M":
                        continue
                case _:
                    continue                    
            count += 1
    return count

# Read the input data from the file
with open('input4.txt', 'r') as f:
    word_search = [line.strip() for line in f]

# Count and print the number of occurrences of XMAS
print(find_all_mas_exes(word_search))

