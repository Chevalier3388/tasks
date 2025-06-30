# Уровень 1
1) На этом уровне разработчик знакомится с базовыми концепциями тестирования в Python и может писать простые тесты.
2) Умеет писать простые unit-тесты с использованием unittest или pytest;
3) Может использовать базовые методы тестирования (assertEqual, assertTrue, assertFalse или assert и др.);
4) Знает как запустить тесты в своем проекте;
5) Понимает как организовывать тесты в файлах и структурах каталогов;


## 1. Базовые концепции тестирования:
### Зачем нужно тестирование?
- Проверка корректности кода.
- Предотвращение регрессий (ошибок при изменениях).
- Упрощение рефакторинга.
- Документирование поведения кода.

### Основные типы тестов:
- Unit-тесты — проверка отдельных функций/методов.
- Интеграционные тесты — проверка взаимодействия компонентов.
- E2E-тесты (End-to-End) — проверка всего приложения целиком.

## 2. Unittest, Pytest

### Unittest
Встроенный модуль для тестирования. Имеет основные компоненты:
- TestCase - базовый класс для тестов.
- setUp() и tearDown() - подготовка и отчистка до/после тестов.
- Методы assert* (assertEqual, assertTrue, и другие).

```python
import unittest

def add(a, b):  # Наша функция
    return a + b

class TestAddFunction(unittest.TestCase):  # Наш класс для проверки, наследуется от TestCase
    def test_add_positive_numbers(self):  # Сам тест
        self.assertEqual(add(2, 3), 5)  # Наличие ожидаемого результата, в первой части наша ф-я во второй значение.

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

if __name__ == '__main__':
    unittest.main()
```
```python
import unittest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestDivide(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)
```
### Pytest
Pytest - это популярная альтернатива unittest. Его плюсы: 
- Более удобный и мощный
- Не требует создания классов (можно писать простые функции)
- Поддержка фикстур (fixtures), параметризации и плагинов
```python
def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2
```
```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```




## 4. Как запустить тесты в своем проекте?
unittest:
```shell
  python -m unittest файл_с_тестами.py
```
pytest:
```shell
  pytest файл_с_тестами.py
```

## 5. Понимает как организовывать тесты в файлах и структурах каталогов;
### Базовая структура проекта
Стандартный подход в Python — отделять код приложения от тестов.


```text
my_project/  
│  
├── my_package/           # Основной код проекта  
│   ├── __init__.py  
│   ├── module1.py  
│   └── module2.py  
│  
├── tests/                # Тесты  
│   ├── __init__.py       (опционально, но полезно для импортов)  
│   ├── test_module1.py  
│   └── test_module2.py  
│  
├── setup.py              (если проект — устанавливаемый пакет)  
└── README.md  
```
- Четкое разделение кода и тестов.
- Удобный импорт (from my_package import ...).
- Совместимость с инструментами (pytest, unittest).

### Подкаталоги для сложных тестов
```text
tests/  
├── unit/  
│   ├── test_module1.py  
│   └── test_module2.py  
├── integration/  
│   └── test_api.py  
└── e2e/  
    └── test_ui.py  
```
- Четкое разделение типов тестов.
- Удобно для CI/CD (можно запускать только юнит-тесты).

### Пример полной структуры
```text
project/  
├── src/  
│   └── my_package/  
│       ├── __init__.py  
│       ├── utils.py  
│       └── api.py  
│  
├── tests/  
│   ├── unit/  
│   │   ├── test_utils.py  
│   │   └── conftest.py  
│   ├── integration/  
│   │   └── test_api.py  
│   └── e2e/  
│       └── test_ui.py  
│  
├── pyproject.toml  
└── README.md  
```

- Отделяйте тесты от основного кода (папка tests/).
- Используйте ```__init__.py```, если нужны относительные импорты.
- Группируйте тесты (unit, integration, e2e).
- Запускайте тесты через pytest — он гибче unittest.
