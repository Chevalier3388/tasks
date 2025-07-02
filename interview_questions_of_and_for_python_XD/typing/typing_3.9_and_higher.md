from tkinter.font import names

# Параметризованные типы и аннотации коллекций
## Типизация списков, словарей и кортежей
Типизация нужна, чтобы ```mypy``` понимал, какие типы данных хранятся в коллекциях.
```python
from typing import List, Dict, Tuple
# Устарело
names: List[str] = ["Alice", "Bob"]
user_ages: Dict[str, int] = {"Alice": 25, "Bob": 30}
coordinates: Tuple[float, float] = (10.5, -20.3)

# Альтернативно (Python 3.9+):
names: list[str] = ["Alice", "Bob"]
user_ages: dict[str, int] = {"Alice": 25, "Bob": 30}
coordinates: tuple[float, float] = (10.5, -20.3)
```
Без типизации можно случайно положить число в ```names```, и ```mypy``` не заметит ошибку:
```python
names.append(69)  # Без типизации это пройдёт
```
## Union (или | в Python 3.10+) — когда тип может быть разным
Если функция принимает либо строку, либо число.
```python
from typing import Union
# Устарело
def process_data(data: Union[str, int]) -> None:
    print(data)

# Альтернативно (Python 3.10+):
def process_data(data: str | int) -> None:
    print(data)
```
```python
from typing import Union
# Устарело
def parse_input(value: Union[str, int]) -> int:
    return int(value)

# Альтернатива в Python 3.10+
def parse_input(value: str | int) -> int:
    return int(value)

parse_input("123")  # OK
parse_input(123)    # OK
parse_input([1, 2]) # Ошибка mypy: List не входит в Union
```
- Используется в API где поле может быть определённым типом, или ```None```. 
- Так же в функциях, которые работают с разными типами входных данных.
##  Optional — когда значение может быть None
Используется, чтобы явно показать, что переменная либо имеет тип, либо None.

Пример: поиск пользователя в базе
```python
from typing import Optional
# Устарело
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None  # OK, потому что Optional[str]

# Альтернатива в Python 3.10+
def find_user(user_id: int) -> str | None:
    ...
```
Чем отличается от Union[str, None]?
Ничем! Optional[str] — это просто удобный алиас для Union[str, None].

## Callable — типизация функций как аргументов

```python
from typing import Callable

def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

apply_func(lambda x, y: x + y, 3, 5)  # 8
```
Используется, чтобы передавать функции в другие функции и сохранять проверку типов.

Пример: функция-фильтр:
```python
from typing import Callable

def filter_numbers(
    numbers: list[int],
    condition: Callable[[int], bool]  # Функция, которая принимает int и возвращает bool
) -> list[int]:
    return [n for n in numbers if condition(n)]

# Использование
filter_numbers([1, 2, 3], lambda x: x > 1)  # Вернёт [2, 3]
```
- В сортировках (key= функции).
- В обработчиках событий (например, on_click).
## TypeAlias — для сложных типов
```python
from typing import TypeAlias

UserId: TypeAlias = int
UserName: TypeAlias = str

def get_user(id: UserId) -> UserName:
    return "Alice"
```
Чтобы давать понятные имена сложным типам, например:
```python
from typing import TypeAlias, Dict, List

# Без TypeAlias
def process_data(data: Dict[str, List[tuple[int, str]]]) -> None:
    ...

# С TypeAlias
UserData: TypeAlias = dict[str, list[tuple[int, str]]]  # Актуально

def process_data(data: UserData) -> None:
    ...
```
- Уменьшает дублирование.
- Делает код читаемее.
## Generator и AsyncGenerator — для генераторов
Чтобы типизировать функции, которые возвращают генераторы.
### Generator[YieldType, SendType, ReturnType] | Генератор[Тип вывода, тип отправки, тип возврата]
- YieldType — что генератор возвращает при yield
- SendType — что можно передать в генератор через .send()
- ReturnType — что возвращает return в генераторе

Пример: генератор чисел
```python
from typing import Generator

def count_up_to(n: int) -> Generator[int, None, None]:  
    for i in range(n):
        yield i  # Порождает int

# Использование
for num in count_up_to(5):
    print(num)  # mypy знает, что num — int
```
Асинхронный вариант:
### AsyncGenerator[YieldType, SendType]
- YieldType — что возвращает yield (например, int, str, dict).
- SendType — что можно передать через .asend() (если не нужно — None).
```python
from typing import AsyncGenerator
import asyncio

async def async_count() -> AsyncGenerator[int, None]:
    for i in range(3):
        yield i
        await asyncio.sleep(1)

# Использование
async for num in async_count():
    print(num)
```
### Где всё это применяется в реальных проектах?
- Списки и словари — почти везде, где есть данные. ```list[int]``` лучше, чем просто ```list```.
- Union / Optional — в API, базах данных, конфигах. ```Optional``` — это Union[T, None].
- Callable — в обработчиках событий, декораторах. ```Callable``` нужен, чтобы передавать функции как аргументы.
- TypeAlias — для сложных структур данных (JSON, CSV). ```TypeAlias``` делает код чище.
- Generator — в ETL-пайплайнах, обработке больших данных. ```Generator``` типизирует yield-функции.


