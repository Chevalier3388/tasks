# [1, 2, 3]
# [8, 9, 4]
# [7, 6, 5]


import numpy as np


def create_spiral(n):
    matrix = np.zeros((n, n), dtype=int)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # право, низ, лево, верх
    current_dir = 0
    x, y = 0, 0

    for num in range(1, n * n + 1):
        matrix[x, y] = num

        # Пробуем двигаться в текущем направлении
        dx, dy = directions[current_dir]
        nx, ny = x + dx, y + dy

        # Если достигли границы или уже заполненной ячейки - меняем направление
        if nx < 0 or nx >= n or ny < 0 or ny >= n or matrix[nx, ny] != 0:
            current_dir = (current_dir + 1) % 4
            dx, dy = directions[current_dir]
            nx, ny = x + dx, y + dy

        x, y = nx, ny

    return matrix


# Тестируем для n=3
spiral = create_spiral(4)
print(spiral)



