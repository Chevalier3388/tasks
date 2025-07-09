# Concatenate (часть PEP 612)
Позволяет добавлять или изменять параметры в сигнатуре функции. 
Особенно полезен для декораторов, которые модифицируют аргументы.

```python
from typing import Concatenate, Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

# Декоратор, добавляющий строковый аргумент в начало
def add_arg(func: Callable[P, R]) -> Callable[Concatenate[str, P], R]:
    def wrapper(s: str, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Добавлен аргумент: {s}")
        return func(*args, **kwargs)
    return wrapper

@add_arg
def multiply(a: int, b: int) -> int:
    return a * b

multiply("test", 3, 4)  # Теперь первый аргумент — строка
```
