# Уровень 2
1) На этом уровне разработчик понимает важность тестирования различных частей системы и может писать тесты разных уровней.
2) Знает про fixtures и умеет использовать их для упрощения тестов
3) Понимает, что такое mocking, и использует unittest.mock для замены зависимостей в тестах
4) Умеет проверять исключения в тестах with pytest.raises(ValueError)
5) Может писать параметризованные тесты для проверки множества сценариев @pytest.mark.parametrize
6) Пирамида тестирования. Модульные тесты, Интеграционные тесты, End-to-End тесты. Основная суть, преимущества, недостатки

## 1. На этом уровне разработчик понимает важность тестирования различных частей системы и может писать тесты разных уровней.
### 1. Unit-тесты (Модульные тесты)
- Что тестируют? Отдельные функции/классы изолированно от внешних зависимостей.
```python
# tests/unit/test_math_utils.py

def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2
```
Запуск:
```shell
  pytest tests/unit/
```
### 2. Интеграционные тесты
- Что тестируют? Взаимодействие нескольких компонентов (например, функция + БД, API + сервис).
```python
# my_package/db.py
class Database:  # Класс БД
    def get_user(self, user_id):  # Функция для получения из бд
        return {"id": user_id, "name": "Test User"}
```
```python
# my_package/api.py
from my_package.db import Database  # Импорт модулей

def get_username(user_id):  # Функция для обращения к бд
    db = Database()
    return db.get_user(user_id)["name"]
```
```python
# tests/integration/test_api_db.py
from my_package.api import get_username  # Импорт модулей

def test_get_username():  # Тест функции которая обращается к бд
    assert get_username(1) == "Test User"
```
Запуск:
```shell
    pytest tests/integration/
```
### 3. End-to-End (E2E) тесты
- Что тестируют? Полный рабочий поток приложения (например, веб-запрос → обработка → ответ).

```python
# main.py (FastAPI app)
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```
```python
# tests/e2e/test_app.py
import requests

def test_root_endpoint():
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```
Запуск сервера:
```shell
  uvicorn main:app --reload
```
Запуск:
```shell
  pytest tests/e2e/
```

- Unit	Отдельные функции	add(2, 3) == 5
- Integration	Взаимодействие компонентов	API + БД, Сервис A → Сервис B
- E2E	Полный сценарий	Веб-запрос → Ответ

## 2. Знает про fixtures и умеет использовать их для упрощения тестов
***Фикстуры*** (fixtures) в pytest — это мощный инструмент для подготовки данных, мокирования зависимостей и переиспользования кода в тестах.

Основные возможности:
- Инициализация ресурсов (БД, API-клиенты, временные файлы).
- Очистка после тестов (автоматический вызов teardown).
- Переиспользование в разных тестах.

```python
import pytest

# Фикстура, которая возвращает список чисел
@pytest.fixture
def sample_numbers():  # sample_numbers выполняется перед каждым тестом, где она указана.
    return [1, 2, 3, 4, 5]

# Тест использует фикстуру как параметр
def test_sum(sample_numbers):  # Результат передаётся в тест как аргумент.
    assert sum(sample_numbers) == 15

def test_len(sample_numbers):  # Результат передаётся в тест как аргумент.
    assert len(sample_numbers) == 5
```
### Фикстуры с setup и teardown
Если фикстура создаёт ресурс (например, файл или соединение с БД), его нужно очистить после теста.

```python
import pytest
import os

@pytest.fixture
def temp_file(tmp_path):  # tmp_path — встроенная фикстура pytest
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Hello, pytest!")
    yield file_path  # Тест получает file_path
    os.remove(file_path)  # Очистка после теста

def test_file_content(temp_file):
    with open(temp_file, "r") as f:
        content = f.read()
    assert content == "Hello, pytest!"
```
yield — разделяет код на setup (до теста) и teardown (после теста).

Как работает tmp_path:
Pytest автоматически создаёт уникальный временный каталог перед началом теста и очищает его после завершения. 
Это позволяет:
- Изолировать тесты — каждый тест получает свой собственный временный каталог, что предотвращает конфликты. 
- Автоматически удалять временные файлы и каталоги — нет необходимости вручную управлять удалением.
- Работать кроссплатформенно — путь к каталогу не зависит от операционной системы. 

### Общие фикстуры (conftest.py)
Если фикстура нужна во многих тестах, её можно вынести в conftest.py — pytest найдёт её автоматически.
```text
project/
├── tests/
│   ├── conftest.py          # Фикстуры доступны всем тестам
│   ├── unit/
│   │   └── test_math.py
│   └── integration/
│       └── test_api.py
```
```python
# project/tests/conftest.py
import pytest

@pytest.fixture
def mock_user():
    return {"id": 1, "name": "Alice"}
```
```python
def test_user_name(mock_user):
    assert mock_user["name"] == "Alice"
```

### Параметризация фикстур
Фикстура может возвращать разные данные для разных тестов.
```python
import pytest

@pytest.fixture(params=["apple", "banana", "orange"])
def fruit(request):
    return request.param  # request — специальный объект pytest

def test_fruit_length(fruit):
    assert len(fruit) >= 5
```
Запуск:
```shell
    pytest test_fruit.py -v
```
```text
test_fruit.py::test_fruit_length[apple] PASSED
test_fruit.py::test_fruit_length[banana] PASSED
test_fruit.py::test_fruit_length[orange] PASSED
```

## 3. Понимает, что такое mocking, и использует для замены зависимостей в тестах
### Фикстуры для мокирования (подмены зависимостей)
Часто нужно заменить реальный API или БД на заглушку. Пример: Мокирование API-запроса
```python
import pytest
import requests

def fetch_data():
    response = requests.get("https://api.example.com/data")
    return response.json()

# Фикстура-мок
@pytest.fixture
def mock_response(monkeypatch):
    def fake_get(*args, **kwargs):
        return {"data": "test"}

    monkeypatch.setattr(requests, "get", fake_get)

def test_fetch_data(mock_response):
    assert fetch_data() == {"data": "test"}
```
```monkeypatch``` подменяет requests.get на fake_get только на время теста.

Пример: ```capsys``` для перехвата вывода
```python
def greet(name):
    print(f"Hello, {name}!")

def test_greet(capsys):
    greet("Alice")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Alice!\n"
```
Практические советы:
- Не делайте фикстуры слишком сложными — они должны быть понятными.
- Используйте conftest.py для общих фикстур.
- Фикстуры с yield — для ресурсов с очисткой.
- Мокируйте внешние зависимости (API, БД) для изоляции тестов.

## 4. Умеет проверять исключения в тестах with pytest.raises(ValueError)
### 1. Базовый пример: pytest.raises()
Допустим, у нас есть функция, которая бросает ValueError, если делитель равен нулю:
```python
# math_operations.py
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
```
```python
import pytest
from math_operations import divide

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)  # Должно вызвать ValueError
```
Что проверяет этот тест?
- ✅ Код divide(10, 0) вызывает ValueError.
- ❌ Если исключение не возникнет — тест упадёт.
### 2. Проверка нескольких исключений
Если функция может вызывать разные исключения, можно проверить их по отдельности:
```python
# math_operations.py
def sqrt(x: float) -> float:
    if x < 0:
        raise ValueError("x must be non-negative")
    if x == 0:
        raise ArithmeticError("x cannot be zero")
    return x ** 0.5
```
```python
def test_sqrt_negative():
    with pytest.raises(ValueError):
        sqrt(-1)

def test_sqrt_zero():
    with pytest.raises(ArithmeticError):
        sqrt(0)
```

- Всегда проверяйте тип исключения.
- Можно проверять текст ошибки (match).
- Используйте as exc_info, если нужны детали исключения.



## 5. Может писать параметризованные тесты для проверки множества сценариев @pytest.mark.parametrize
### 1. Базовый пример: @pytest.mark.parametrize
Допустим, у нас есть функция add(a, b), и мы хотим проверить её на нескольких наборах данных.
```python
# math_ops.py
def add(a: int, b: int) -> int:
    return a + b
```
```python
import pytest
from math_ops import add

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),      # a=2, b=3 → expected=5
    (0, 0, 0),      # 0 + 0 = 0
    (-1, 1, 0),     # -1 + 1 = 0
    (10, -5, 5),    # 10 + (-5) = 5
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```
Как это работает?
- Декоратор @pytest.mark.parametrize принимает:
Имена аргументов ("a, b, expected").
Список кортежей с тестовыми данными.
- pytest запустит test_add() 4 раза с разными (a, b, expected).
```text
test_math.py::test_add[2-3-5] PASSED
test_math.py::test_add[0-0-0] PASSED
test_math.py::test_add[-1-1-0] PASSED
test_math.py::test_add[10--5-5] PASSED
```
### 2. Параметризация с разными типами данных
Можно тестировать не только числа, но и строки, списки и другие типы.
```python
# string_ops.py
def concat(str1: str, str2: str) -> str:
    return str1 + str2
```
```python
import pytest
from string_ops import concat

@pytest.mark.parametrize("str1, str2, expected", [
    ("hello", " world", "hello world"),
    ("", "test", "test"),          # Пустая строка
    ("123", "456", "123456"),      # Числа как строки
])
def test_concat(str1, str2, expected):
    assert concat(str1, str2) == expected
```
### 3. Параметризация + проверка исключений
Можно комбинировать parametrize с pytest.raises().
```python
# math_ops.py
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b
```
```python
import pytest
from math_ops import divide

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),                 # Успешный случай
    (0, 1, 0),                  # 0 / 1 = 0
    (10, 0, ValueError),        # Деление на 0 → ошибка
    ("10", 2, TypeError),       # Неправильный тип → ошибка
])
def test_divide(a, b, expected):
    if expected in (ValueError, TypeError):
        with pytest.raises(expected):
            divide(a, b)
    else:
        assert divide(a, b) == expected
```
Что происходит?
- Если expected — это тип исключения, тест проверяет, что оно возникает.
- Иначе — сравнивает результат с expected.
### 4. Параметризация из внешнего источника
Можно вынести тестовые данные в отдельную функцию или файл.
```python
def get_test_data():
    return [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
    ]

@pytest.mark.parametrize("a, b, expected", get_test_data())
def test_add_from_data(a, b, expected):
    assert add(a, b) == expected
```
```python
import json
import pytest

def load_test_data():
    with open("test_data.json") as f:
        return json.load(f)

@pytest.mark.parametrize("a, b, expected", load_test_data())
def test_add_from_json(a, b, expected):
    assert add(a, b) == expected
```
Главные преимущества:
- Уменьшение дублирования кода — один тест для множества сценариев.
- Удобный вывод — каждый случай отображается отдельно.
- Гибкость — можно комбинировать с фикстурами, проверкой ошибок и т. д.

## 6. Пирамида тестирования. Модульные тесты, Интеграционные тесты, End-to-End тесты. Основная суть, преимущества, недостатки.
### 4 уровня тестирования:
Модульные тесты
Преимущества:
- ✅ Быстрые — выполняются за миллисекунды.
- ✅ Стабильные — не зависят от внешних систем.
- ✅ Помогают найти баги на раннем этапе.

Недостатки:
- ❌ Не проверяют взаимодействие компонентов.
- ❌ Могут пропускать системные ошибки.

Доля в пирамиде: ~70% (основа).
 - 1-й. Модульное тестирование (Unit Testing)
***цель*** этого уровня протестировать каждую условную единицу кода (модуль, пакет, функция)
***разрабатывается*** на этапе написания кода

Интеграционные тесты
Преимущества:
- ✅ Проверяют корректность интеграции.
- ✅ Обнаруживают проблемы API, БД, сетевых вызовов.

Недостатки:
- ❌ Медленнее unit-тестов.
- ❌ Требуют настройки внешних зависимостей (например, тестовой БД).

Доля в пирамиде: ~20%.
- 2-й. Интеграционное тестирование (Integration Testing)
***цель*** этого уровня протестировать взаимодействие объединённых групп модулей (бэк и бд)
***разрабатывается*** после модульного тестирования, когда большая часть кода проверена изолированно.

End-to-End тесты
Преимущества:
- ✅ Проверяют систему как единое целое.
- ✅ Самые близкие к реальному пользовательскому опыту.

Недостатки:
- ❌ Очень медленные (секунды или минуты на тест).
- ❌ Хрупкие — могут ломаться из-за изменений в UI/API.
- ❌ Сложные в отладке.

Доля в пирамиде: ~10%.
- 3-й. Системное тестирование (System Testing)
***цель*** этого уровня проверить систему в целом с точки зрения конечных пользователей. Особое 
внимание уделяется бизнес функциям (функции с которыми работают пользователи).
на этом этапе учитывают нагрузки и скорость работы сервиса. 
***разрабатывается*** комплексное тестирование, где мы тестируем нашу систему в целом. 

- 4-й. Приёмочное тестирование (Acceptance Testing (UserAT))
***цель*** этого уровня проверить соблюдение архитектурных стандартов, проверка выполнения всех функций из тз, 
проверить безопасность соответствующим отделом

### Как применять пирамиду на практике?
- Покрывайте unit-тестами всю бизнес-логику.
- Добавляйте интеграционные тесты для ключевых взаимодействий (API + БД).
- Пишите E2E-тесты только для критических пользовательских сценариев (например, оформление заказа).

Пример для веб-приложения:
- Unit: Проверка расчёта скидки в корзине.
- Integration: Проверка, что заказ сохраняется в БД.
- E2E: Полный цикл: вход → выбор товара → оплата.

Пирамида помогает экономить время и снижать риски — больше тестов на нижних уровнях, меньше на верхних. 🚀
