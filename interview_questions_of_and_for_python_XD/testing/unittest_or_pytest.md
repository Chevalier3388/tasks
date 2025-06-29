***unittest или pytest*** - это базовые инструменты для unit-тестов.
Разница состоит в том:
- unittest встроенный в Python модуль для тестирования, а pytest внешняя библиотека.
- unittest требует создания классов, наследования от unittest.TestCase, а pytest работает с обычными функциями.
- unittest менее гибкий, но стандартизированный а pytest более мощный и удобный (фикстуры, параметризация)

Пример:

Дана функция:
```python
# src/calculator.py

def divide(a, b):
    if b == 0:
        raise ValueError("Нельзя делить на ноль!")
    return a / b
```

Unittest:
```python
# tests/test_calc_unittest.py
import unittest
from src.calculator import divide

class TestCalculator(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)  # Проверка равенства

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):  # Проверка исключения
            divide(10, 0)

if __name__ == "__main__":
    unittest.main()
```
Запустить:
```shell
  python -m unittest tests/test_calc_unittest.py
```

Pytest:
```python
# tests/test_calc_pytest.py
import pytest
from src.calculator import divide

def test_divide():
    assert divide(10, 2) == 5  # Простой assert

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Нельзя делить на ноль!"):  
        divide(10, 0)
```
Запустить:
```shell
    pytest tests/test_calc_pytest.py -v
```
