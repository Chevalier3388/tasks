Получил задачу от своего наставника: сделай декоратор, да так, что бы вывод был таким, какой я указал в примере.
И тут всё началось...

```python
"""
Написать реализацию декоратора для измерения и логирования времени работы произвольной функции. 
Декоратор не должен изменять поведение функции.
В примере представлена функция f для которой нужно реализовать декоратор timeit, 
а ниже даны примеры результатов логирования после вызова функции.

f(1)
[INFO] f(1): 1.1 sec


f('1')
[ERROR] f('1'): 0.1 sec
"""
import logging
import time
logger = logging.getLogger()



# TODO ...


@timeit(logger)
def f(s):
    time.sleep(s)
    return 5


def main():
    f(1)
    f('1')


if __name__ == '__main__':
    main()
```

Декоратор - это функция, которая добавляет новую функциональность к другой функции без изменения её кода.

Декоратор - функция, которая оборачивает другую функцию 
для расширения её функциональности без непосредственного изменения её кода.

Декоратор – это функция высшего порядка, 
которая принимает функцию и добавляет в результат что-нибудь от себя, не вмешиваясь в логику полученной функции


Моя первая реализация была просто огромна!
```python
from functools import wraps
import logging
import time
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("my_loger")



def timeit(log):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            try:
                res = func(*args, **kwargs)
                stop = time.time()
                log.info(f"{func.__name__}{args, kwargs}: {round(stop - start, 1)} sec")
                return res
            except:
                stop = time.time()
                return log.error(f"{func.__name__}{args, kwargs}: {round(stop - start, 1)} sec")
        return inner
    return wrapper


@timeit(logger)
def f(s):
    time.sleep(s)
    return 5

def main():
    f(1)
    f('1')


if __name__ == '__main__':
    main()
```

Результат был близким, но не тем, что ожидалось! 
```
INFO f((1,), {}): 1.0 sec
ERROR f(('1',), {}): 0.0 sec
```
- первое отличие - это наличие разных скобок. Их не должно быть столько!
- второе это менее очевидное, функция меняет своё поведение! 
А по условию: "Декоратор не должен изменять поведение функции."
Если добавим принты для проверки(можно и логи)
```python
def main():
    value = f(1)
    print(value)
    value_error = f('1')
    print(value_error)
```
То в выводе мы увидим, как место ожидаемого результата, функция со строкой возвращает None.
```
5
None
```







[ссылка "https://proglib.io"](https://proglib.io/p/samouchitel-po-python-dlya-nachinayushchih-chast-14-funkcii-vysshego-poryadka-zamykaniya-i-dekoratory-2023-01-30)