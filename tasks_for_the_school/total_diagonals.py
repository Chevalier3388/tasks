def total_diagonals(n):
    return int(0.5 * n * (n - 3))

if __name__ == "__main__":
    d = int(input("Введите количество углов в многоугольнике: "))

    print(total_diagonals(d))