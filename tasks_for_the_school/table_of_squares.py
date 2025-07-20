def print_square_table(width, height):
    """
    Печатает таблицу квадратов чисел, составленных из номера строки и столбца
    :param width: количество столбцов (начинаются с 0)
    :param height: количество строк (начинаются с 1)
    """
    # Создаем таблицу значений
    table = []
    for row in range(1, height + 1):
        row_data = []
        for col in range(0, width + 1):  # +1 чтобы включить последний столбец
            num = int(f"{row}{col}")
            squared = num ** 2
            row_data.append(squared)
        table.append(row_data)

    # Определяем ширину каждой колонки
    col_widths = [max(len(str(col)), len(str(0))) for col in range(0, width + 1)]
    for row in table:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # Функция для создания горизонтальной линии
    def make_horizontal_line():
        parts = ["+"]
        for width in col_widths:
            parts.append("-" * (width + 2))
            parts.append("+")
        return "".join(parts)

    # Функция для создания двойной линии
    def make_double_line():
        parts = ["+"]
        for width in col_widths:
            parts.append(" -" * ((width + 2) // 2) + " -"[:((width + 2) % 2)])
            parts.append("+")
        return "".join(parts)

    # Верхняя граница
    print(make_double_line())

    # Заголовок колонок
    header = "|" + " " * 6 + "|"
    for col in range(0, width + 1):
        header += f" {col:^{col_widths[col]}} |"
    print(header)

    # Разделитель заголовка
    print(make_double_line())

    # Тело таблицы
    for row_num in range(1, height + 1):
        # Номер строки
        line = f"| {row_num:^4} |"

        # Значения в строке
        for col_num in range(0, width + 1):
            val = table[row_num - 1][col_num]
            line += f" {val:^{col_widths[col_num]}} |"

        print(line)

        # Разделитель строк
        if row_num < height:
            print(make_double_line())
        else:
            print(make_horizontal_line())


# Пример использования:
print_square_table(9, 9)
print_square_table(5, 3)