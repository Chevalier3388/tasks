## Параметризованные тесты в pytest

Параметризация позволяет запускать один тест для множества входных данных. 
Это идеально для проверки граничных условий и разных сценариев.

### Базовый синтаксис
```python
import pytest

@pytest.mark.parametrize("input_a, input_b, expected", [
    (1, 2, 3),       # Кортеж 1
    (0, 0, 0),       # Кортеж 2
    (-1, 1, 0),      # Кортеж 3
])
def test_add(input_a, input_b, expected):
    assert input_a + input_b == expected
```
- Тест выполнится 3 раза — для каждого набора параметров
- Имена параметров (input_a, input_b, expected) должны совпадать в декораторе и аргументах функции

### Разные типы данных
```python
@pytest.mark.parametrize("value, expected", [
    ("hello", 5),        # Строка
    ([1, 2, 3], 3),      # Список
    ({"a": 1}, 1),       # Словарь
])
def test_len(value, expected):
    assert len(value) == expected
```
### Комбинации параметров
```python
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [10, 20])
def test_multiply(a, b):
    assert a * b == (a * b)  # Проверит все комбинации: (1,10), (1,20), (2,10), (2,20)
```
### Параметризация + фикстуры
```python
@pytest.fixture
def multiplier():
    return 2

@pytest.mark.parametrize("input_num, expected", [
    (1, 2),
    (5, 10),
])
def test_multiply_by_fixture(input_num, expected, multiplier):
    assert input_num * multiplier == expected
```
### Параметризация классов
```python
@pytest.mark.parametrize("browser", ["chrome", "firefox"])
class TestLogin:
    def test_login_valid(self, browser):
        print(f"Тест в {browser}")  # Запустится для каждого браузера

    def test_login_invalid(self, browser):
        assert browser in ["chrome", "firefox"]
```
### Чтение параметров из файла
Файл ```data.json```
```json
[
    {"input": "hello", "expected": 5},
    {"input": "world", "expected": 5}
]
```
Файл ```test_from_file.py```
```python
import json

with open("data.json") as f:
    test_data = json.load(f)

@pytest.mark.parametrize("data", test_data, ids=lambda x: f"input={x['input']}, expected={x['expected']}")
def test_from_file(data):
    assert len(data["input"]) == data["expected"]
```
Структура:
```text
project/
├── data.json
└── test_from_file.py
```
Запустить:
```shell
  pytest test_from_file.py -v
```
Ожидаемый ответ:
```text
collected 2 items                                                                                                                                                      

task_test.py::test_from_file[input=hello, expected=5] PASSED [ 50%]
task_test.py::test_from_file[input=world, expected=5] PASSED [100%]

========================= 2 passed in 0.06s========================
```
### ```pytest.param()```
```pytest.param()``` для маркировки отдельных наборов:
```python
@pytest.mark.parametrize("a, b, expected", [
    pytest.param(1, 2, 3, id="positive"),
    pytest.param(0, 0, 0, id="zeros"),
])
```
### Когда использовать
- При проверке граничных значений
- При разных типах входных данных
- Когда нужны комбинаторные проверки
- Тестирование API

### Вывод
Параметризация — мощный инструмент для уменьшения дублирования кода и увеличения покрытия тестами.