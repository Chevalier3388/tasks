
# Руководство взял из: https://otvet.mail.ru/question/188763117 XD
# 1, 21, 31... программист
# 2 - 4, 22 - 24, 32 - 34 ... программиста
# 5 - 10, 25 - 30, 35 - 40, 45 - 50 ... программистов

def msg(n: int) -> str:
    if n == 0:
        return "В комнате нет программистов"

    exceptions = {11, 12, 13, 14}
    last_two = n % 100
    last_digit = n % 10

    my_dict: dict[int: str] = {
    0: 'программист',
    1: 'программиста',
    2: 'программистов'
    }
    if last_two in exceptions or last_digit == 0 or last_digit >= 5:
        return f"В комнате {n} программистов"

    return "В комнате {} {}".format(n, my_dict.get(sum([last_digit > 1, last_digit > 4, last_digit > 5]), 'программистов'))

if __name__ == "__main__":
    for i in range(1001):
        print(msg(i))





