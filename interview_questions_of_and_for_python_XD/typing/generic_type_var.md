# TypeVar
TypeVar — это инструмент для создания обобщённых (generic) типов в Python. 
Он позволяет параметризировать функции и классы, сохраняя статическую типизацию.
### история:
- Появился в Python 3.5+ (PEP 484 — Type Hints).
- До этого использовались абстрактные типы (Any, Union), но без гибкости Generics.
- Аналог дженериков в Java (T), TypeScript (<T>), Rust (fn foo<T>()).

### Синтаксис и параметры
```python
from typing import TypeVar, Generic

# Базовый синтаксис:
T = TypeVar('T')  # Произвольный тип
K = TypeVar('K')  # Тип ключа (например, в словаре)
V = TypeVar('V')  # Тип значения

# С ограничениями:
Number = TypeVar('Number', int, float)  # Только int или float
AnyStr = TypeVar('AnyStr', str, bytes)  # Только str или bytes
```
```python
from typing import TypeVar

T = TypeVar("T")  # "T" — имя переменной типа (для аннотаций)

def first_element(items: list[T]) -> T:
    return items[0]
```
- "T" — имя переменной типа (для аннотаций)
- T — это обобщённый тип (Generic), который заменяется на конкретный тип при вызове функции.
- list[T] означает: «Функция принимает список элементов одного типа T и возвращает элемент этого же типа».
## Параметры ```TypeVar```
### Имя ('T'):
- Условное обозначение (обычно T, K, V, U).
- Важно для читаемости (например, Dict[K, V]).
### bound= (ограничение сверху):
```python
T = TypeVar('T', bound=int | float)  # Любой подтип int или float
```
### Конкретные типы (альтернатива ```bound```):
```python
T = TypeVar('T', str, bytes)  # Только str или bytes
```
## Правила использования
###  В функциях
```python
from typing import List, TypeVar

T = TypeVar('T')

def first_element(items: List[T]) -> T:
    return items[0]

first_element([1, 2, 3])    # int
first_element(["a", "b"])   # str
```
### В классах (Generic-классы)
```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item

box_int = Box(123)     # Box[int]
box_str = Box("hello") # Box[str]
```
### Ограничение типов (bound=)
```python
from typing import TypeVar, Union

Numeric = TypeVar('Numeric', bound = int | float)

def add(a: Numeric, b: Numeric) -> Numeric:
    return a + b

add(3, 5)      # OK
add(2.5, 1.5)  # OK
add("a", "b")  # Ошибка типов
```
### Множественные TypeVar
```python
K = TypeVar('K')  # Тип ключа
V = TypeVar('V')  # Тип значения

def get_value(d: dict[K, V], key: K) -> V:
    return d[key]

get_value({"a": 1, "b": 2}, "a")  # int
```

