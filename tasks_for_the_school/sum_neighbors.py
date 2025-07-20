

# input -> "3 5 6 10"
# output -> "13 6 9 15 7"

def sum_of_neighbors(string: str) -> str:
    s = string.split()
    l = len(s)
    return " ".join([str(int(s[i - 1]) + int(s[(i + 1)%l])) for i in range(len(s))])

print(sum_of_neighbors("1 2 3 4 5 6 7 8 9 10"))