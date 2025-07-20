import math


class Figure:
    def get_perimeter(self):
        """Базовый метод для получения периметра фигуры"""
        raise NotImplementedError("Этот метод должен быть переопределен в дочерних классах")


class Rectangle(Figure):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def get_perimeter(self):
        return 2 * (self.length + self.width)


class Square(Figure):
    def __init__(self, side):
        self.side = side

    def get_perimeter(self):
        return 4 * self.side


class Circle(Figure):
    def __init__(self, radius):
        self.radius = radius

    def get_perimeter(self):
        return 2 * math.pi * self.radius


class Triangle(Figure):
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def get_perimeter(self):
        return self.side1 + self.side2 + self.side3


# Пример использования
if __name__ == "__main__":
    pass