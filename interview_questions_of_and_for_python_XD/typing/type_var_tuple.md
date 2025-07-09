# ```TypeVarTuple``` (PEP 646)
Позволяет работать с переменным количеством типов 
(аналог *args, но для типов). Полезен для функций, 
принимающих произвольное количество аргументов с разными типами 
(например, numpy.array или zip).

```python
from typing import TypeVarTuple

Ts = TypeVarTuple('Ts')  # Тип-кортеж

def process_tuple(*args: *Ts) -> tuple[*Ts]:
    return args

x: tuple[int, str, bool] = process_tuple(1, "hello", True)  # OK!
```

Функции с переменным числом аргументов разного типа. Пример: Аналог zip или map.
```python
Ts = TypeVarTuple('Ts')

def zip_with_types(*args: *tuple[*Ts]) -> tuple[*Ts]: ...
```

# ```Unpack```
```Unpack``` — это оператор для распаковки TypeVarTuple в аннотациях.
```python
from typing import TypeVarTuple, Unpack

Ts = TypeVarTuple('Ts')

def process(*args: *Ts) -> tuple[Unpack[Ts]]:  # Аналог Tuple[*Ts]
    return args
```
В функциях высшего порядка
```python
def apply(func: Callable[[Unpack[Ts]], R], *args: *Ts) -> R:
    return func(*args)
```
- ```TypeVar``` — один тип, ```TypeVarTuple``` — несколько (как ```*args``` для типов).
- ```Unpack``` нужен для распаковки TypeVarTuple в аннотациях (```Tuple[*Ts]``` → ```Tuple[Unpack[Ts]]```).
- ```*Ts``` и ```Unpack[Ts]``` одно и тоже, но ```Unpack``` явно указывает на распаковку.
- Unpack можно использовать только с ```TypeVarTuple```
- 