# Вам необходимо найти длину самого длинного палиндрома в записи.
# Формат ввода:
# Строка содержит n целых чисел a₁, a₂, ..., aₙ (1 ≤ aᵢ ≤ 1 0 9 10^9109) — последовательность.
# Формат вывода
# Выведите одно целое число — длину самого длинного палиндрома в записи. Если такого нет, выведите 0.

def pal(string):
    return string == string[::-1] and len(string) > 1


def max_len(string):
    string = string.replace(" ", "")
    print(string)
    lst = []
    for i in range(len(string)):
        for j in range(i, len(string)):
            sub = string[i: j + 1]
            if pal(sub):
                lst.append(len(sub))
    return max(lst) if lst else 0


lst_test_string = ["1 2 3 4 3 2 1", "1 2 3 4 5", "1 2 3 4 5 5 4 3 2 1", "1 2 3 1 2 3", "112"]

for el in lst_test_string:
    print(max_len(el))