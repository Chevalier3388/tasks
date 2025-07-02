# Generator[YieldType, SendType, ReturnType] — типизация генераторов в Python
## Зачем это нужно?
### Генераторы — это функции с yield, которые могут:
- Возвращать значения (yield x).
- Принимать значения (x = yield).
- Возвращать финальный результат (return).

Чтобы mypy понимал, какие типы используются в этих операциях, нужна аннотация:
```python
Generator[YieldType, SendType, ReturnType]
```
### YieldType — что генератор возвращает при yield
```python
from typing import Generator

def numbers() -> Generator[int, None, None]:
    yield 1
    yield 2
    yield 3

for num in numbers():  # num имеет тип int
    print(num)
```
Что будет, если не указать?
- mypy не поймёт, что num — это int.
### SendType — что можно передать в генератор через .send()
```python
def counter() -> Generator[int, str, None]:
    total = 0
    while True:
        received = yield total  # Принимаем str
        if received == "stop":
            break
        total += 1

gen = counter()
print(next(gen))  # 0
print(gen.send("go"))  # 1
print(gen.send("stop"))  # StopIteration
```
Если генератор не принимает значения:
Используем ```None``` → ```Generator[int, None, None]```.
### ReturnType — что возвращает return в генераторе
```python
def countdown(n: int) -> Generator[int, None, str]:
    while n > 0:
        yield n
        n -= 1
    return "Готово!"

gen = countdown(3)
for num in gen:  # num — int
    print(num)  # 3, 2, 1

try:
    next(gen)
except StopIteration as e:
    print(e.value)  # "Готово!" — это ReturnType
```
### Важно:
- ```return``` в генераторе нельзя использовать как в обычной функции.
- Результат доступен только через ```StopIteration.value```.
## Упрощённые варианты
### Если генератор только возвращает значения (yield):
```python
def numbers(n: int) -> Generator[int, None, None]:
    for i in range(n):
        yield i
```
```YieldType``` = ```int```, остальное None.
### Если генератор только принимает значения (send):
```python
def accumulator() -> Generator[None, int, None]:
    total = 0
    while True:
        value = yield  # Принимает int
        total += value
```
```SendType``` = ```int```, ```YieldType``` = ```None```.
### Если есть return:
```python
def game() -> Generator[str, None, bool]:
    yield "start"
    return True  # Конечный результат
```
```ReturnType``` = ```bool```.
## Реальные примеры
### Чтение файла с прогрессом

```python
from typing import Generator


def read_lines(file_path: str) -> Generator[str, None, int]:
    count = 0
    with open(file_path) as file:
        for line in file:
            yield line.strip()
            count += 1
    return count  # Возвращает количество строк

```
Способ 1. Ловить StopIteration при ручной итерации (без for):
```python
lines_gen = read_lines("../../data.txt")
try:
    while True:
        line = next(lines_gen)
        print(line)
except StopIteration as e:
    print(f"Всего строк: {e.value}")  # int
```
Способ 2. Сохранить значение при завершении цикла:
```python
lines_gen = read_lines("data.txt")
try:
    while True:
        line = next(lines_gen)
        print(line)
except StopIteration as e:
    print(f"Всего строк: {e.value}")  # Теперь получим правильное значение
```
### Альтернативный подход (без return):
Если вам не принципиально использовать return в генераторе, можно просто вернуть кортеж:
```python
def read_lines(file_path: str) -> Generator[str, None, None]:
    count = 0
    with open(file_path) as file:
        for line in file:
            yield line.strip()
            count += 1
    print(f"Всего строк: {count}")  # Просто печатаем значение

# Использование
for line in read_lines("data.txt"):
    print(line)
```
- Используйте либо ручную итерацию с next() и StopIteration,
- либо не полагайтесь на return в генераторе, если используете for.
- Возвращаемое значение return в генераторах — это продвинутая фича, которая требует аккуратного использования.
### Генератор, реагирующий на команды
```python
from typing import Generator

def robot() -> Generator[str, str, str]:
    command = yield "Жду команду..."
    while True:
        if command == "действуй":
            command = yield "Выполняю задание!"
        elif command == "стоп":
            print("Пришла команда СТОП")
            return "Завершился"
        else:
            command = yield "Жду команду..."

r = robot()
print(next(r))  # Инициализирует, без него: "TypeError: can't send non-None value to a just-started generator"
print(r.send("действуй"))
try:
    print(r.send("стоп"))
except Exception as e:
    print(f"Перехвачен в Exception: {e}")
```
## Чем отличается от Iterator?
- ```Iterator[T]``` — только для итераторов с ```__next__```.
- ```Generator``` — для функций с ```yield``` (поддерживает ```send``` и ```return```).
```python
from typing import Iterator

def numbers(n: int) -> Iterator[int]:  # Без send/return
    for i in range(n):
        yield i
```

