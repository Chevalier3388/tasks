

def fib_generator(n: int):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
        yield b

if __name__ == "__main__":

    LIMIT = int(input("Введите число: "))

    for i, num in enumerate(list(fib_generator(LIMIT))):
        print("Fibonacci Numbers №{}: {}".format(i+1, num))