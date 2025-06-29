### Фикстуры — это функции, которые:
- Подготавливают данные для тестов
- Выполняют настройку (setup) и очистку (teardown)
- Позволяют переиспользовать код между тестами
```python
import pytest

def _add(a, b):  # Функция вычитания 
    return a + b

def _subtract(a, b):  # Функция сложения
    return a - b

@pytest.fixture  # Фикстура 10
def num_10():
    return 10

@pytest.fixture  # Фикстура 5
def num_5():
    return 5

def test_add(num_10, num_5):  # Фикстура передается как аргумент
    assert _add(num_10, num_5) == 15
    
def test_subtract(num_10, num_5):  # Фикстура передается как аргумент
    assert _subtract(num_10, num_5) == 5  
```

### Общие фикстуры (conftest.py)
Вынесите в файл tests/conftest.py:
```text
your_project/
├── src/
└── tests/
    ├── conftest.py    ← Вот этот файл
    └── test_example.py
```
```python
# tests/conftest.py

import pytest

@pytest.fixture
def user_data():
    return {"name": "Alice", "age": 30}
```
```python
# tests/test_example.py

def test_user_age(user):
    assert user["age"] == 30  # Фикстура передается как аргумент
```
Как это работает:
- pytest автоматически обнаруживает conftest.py
- Все фикстуры из него становятся доступны в тестах этой папки и всех вложенных

### Иерархия: 
Можно создавать дополнительные conftest.py в подпапках — фикстуры будут доступны только в их зоне:
```text
tests/
├── conftest.py           # Фикстуры для всех тестов
├── api/
│   ├── conftest.py       # Фикстуры только для API-тестов
│   └── test_api.py
└── unit/
    └── test_utils.py
```
Фикстура в локальном conftest.py переопределяет фикстуру из родительского
Правила приоритета:
1. По имени фикстуры:
- Локальная (conftest.py ближе к тесту) переопределяет глобальную.
- Если имена разные — выполнятся обе (порядок: от глобальной к локальной).
2. По autouse:
- Фикстуры с autouse=True выполняются в порядке их обнаружения (глобальная, локальная, тест, локальная, глобальная).
3. Явные vs автоматические:
- Если тест явно запрашивает фикстуру (через аргумент), она выполняется перед autouse-фикстурами.

### Фикстура с настройками (setup, teardown)
Простой пример:
```python
import pytest

def app(data):
    result = f"Использую {data}"
    print(result)
    return result

@pytest.fixture
def my_fixture():
    print("Подготавливаю данные")
    data = "подготовленные данные"  # Настройка (setup)
    yield data                      # Отдаём fixture тесту
    print("Удаляю данные")
    del data                        # Очистка (teardown)

def test_app(my_fixture):
    assert app(my_fixture) == "Использую подготовленные данные"
```
- Всё до yield — настройка
- Всё после yield — уборка
- yield — это момент, когда fixture передаётся тесту
```python
@pytest.fixture
def database():
    conn = create_db_connection()  # Настройка (setup)
    yield conn                     # Передача данных в тест
    conn.close()                   # Очистка (teardown)

def test_query(database):
    assert database.query("SELECT 1") is not None
```
### Scope: контроль времени жизни
Scope определяет, как часто создаётся фикстура:
- function(по умолчанию), фикстура создаётся заново для каждого теста.
```python
@pytest.fixture  # scope="function" по умолчанию
def fresh_data():
    return []
```
- class, фикстура создаётся 1 раз на класс тестов.
```python
@pytest.fixture(scope="class")
def shared_resource():
    return HeavyObject()  # Создаётся 1 раз для всех тестов класса
```
- module, фикстура создаётся 1 раз на файл с тестами.
```python
@pytest.fixture(scope="module")
def db_connection():
    conn = connect_to_db()  # 1 соединение на весь test_*.py
    yield conn
    conn.close()
```
- session, фикстура создаётся 1 раз на все тесты (например, для глобальной конфигурации).
```python
@pytest.fixture(scope="session")
def global_config():
    return load_config()  # Загружается 1 раз при запуске pytest
```
- function — Для изолированных данных (каждый тест получает свою копию).
- class — Если тесты в классе работают с одними и теми же данными.
- module — Для тяжелых ресурсов (БД, API-клиенты).
- session — Для глобальных настроек (токены, конфиги).

Чем выше scope, тем меньше раз создаётся фикстура (ускоряет тесты), но тем менее изолированы тесты друг от друга.

### Автоматические фикстуры
Пример с замером времени:
```python
import pytest
import time
@pytest.fixture(autouse=True)
def time_tracker():
    start = time.perf_counter()
    yield
    print(f"\nТест выполнен за {time.perf_counter() - start:.2f} сек")
```
```python
# Тест 1 (не требует явного вызова фикстуры)
def test_addition():
    print("Проверяем 2+2")
    assert 2 + 2 == 4

# Тест 2 (не требует явного вызова фикстуры)
def test_subtraction():
    print("Проверяем 5-3")
    assert 5 - 3 == 2
```
Вывод будет:
```text
============================= test session starts ==============================
collecting ... collected 2 items
task_test.py::test_addition PASSED      [ 50%]Проверяем 2+2
Тест выполнен за 0.00 сек
task_test.py::test_subtraction PASSED   [100%]Проверяем 5-3
Тест выполнен за 0.00 сек
============================== 2 passed in 0.06s ===============================
Process finished with exit code 0
```
