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
            start = time.monotonic()
            try:
                res = func(*args, **kwargs)
                stop = time.monotonic()
                log.info(f"{func.__name__}{args, kwargs}: {round(stop - start, 1)} sec")
                return res
            except:
                stop = time.monotonic()
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
Первым делом нужно, что бы декоратор возвращал нужное нам значение:
- ```f(1) [INFO] f(1): 1.1 sec```
- ```f('1')[ERROR] f('1'): 0.1 sec```
- 
Для этого мы отредактируем вывод сообщения:
введём дополнительную переменную - flag(она нам будет сигнализировать что выводить):
- Если True - будет INFO
- Если False - будет ERROR

Также воспользуемся конструкцией try, except, finally, else и 
перенесём логику вывода в finally(ибо этот блок конструкции будет в любом случае, не зависимо от обстоятельств)


``` python
def timeit(log):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            flag = True
            start = time.monotonic()
            try:
                return func(*args, **kwargs)
            except:
                flag = False
                raise
            finally:  # Добавили блок и перенесли в него логику вывода информации
                stop = time.monotonic()
                if flag:
                    log.info(f"{func.__name__}{args, kwargs}: {round(stop - start, 1)} sec")
                else:
                    log.error(f"{func.__name__}{args, kwargs}: {round(stop - start, 1)} sec")
        return inner
    return wrapper
```

Это сделало код понятнее для чтения, но результат остался тот же.
```python
{args, kwargs}
```
Нужно изменить данное представление в нашем выводе, ибо сейчас оно демонстрирует:
- ```INFO f((1,), {}): 1.0 sec```
- ```ERROR f(('1',), {}): 0.0 sec```

Для изменения и удобства чтения мы выносим его в отдельную переменную и 
соединяем всё в одну строку с помощью функции ```", ".join()```:

```func_param = ", ".join([repr(arg) for arg in args] + [f"{key}={repr(value)}" for key, value in kwargs.items()])```
А ещё в фоорматируем сам логер, что бы ответ был приближен к заданию:
```python
format="[%(levelname)s] %(message)s"
```
Мы добавили квадратные скобки [ ]

Так же мы вынесли  ```{round(stop - start, 1)}``` в отдельную переменную delta: ```delta = stop - start```

```python
def timeit(log):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.monotonic()
            params_func = ", ".join(
                [repr(arg) for arg in args]
                + [f"{key}={repr(value)}" for key, value in kwargs.items()]
            )
            flag = True
            try:
                return func(*args, **kwargs)
            except:
                flag = False
                raise
            finally:  
                stop = time.monotonic()
                delta = stop - start
                if flag:
                    log.info(f"{func.__name__}({params_func}): {round(delta, 1)} sec")
                else:
                    log.error(f"{func.__name__}({params_func}): {round(delta, 1)} sec")
                
        return inner

    return wrapper
```

Всё работает и ответ показывает то, что мы искали, но чувство, что этого будет мало меня не обманывает! 
Мы начинаем полировать код (Искусство чистого кода)

``` python
finally:  
    stop = time.monotonic()
    if flag:
        log.info(f"{func.__name__}({func_param}): {round(delta, 1)} sec")
    else:
        log.error(f"{func.__name__}({func_param}): {round(delta, 1)} sec")
```
Меняем на конструкцию:
```python
finally: 
    stop = time.monotonic()
    delta = stop - start
    level = logging.INFO if flag else logging.ERROR
    log.log(level, "%s(%s) %.1f sec", func.__name__, func_param, delta)
```
Тут мы меняем конструкцию, проводим рефакторинг кода и убираем тяжёлые участки кода.
Это можно посмотреть используя определённые методы вроде:
1) Memory profiler — это инструмент, который показывает:
- Сколько памяти используется
- Какими строками/функциями кода
- Когда и почему происходит рост использования памяти
2) tracemalloc — встроенный в Python (c 3.4+), отслеживает источники аллокации памяти.
3) objgraph — визуализирует ссылки между объектами.
- Показывает где и какие объекты "застряли" в памяти.
- может отрисовать граф ссылок между объектами.
- Помогает понять, почему объект не удаляется — на него может остаться неожиданная ссылка.

Первое и очень важное, мы ушли от использования методов: 
- log.info
- log.error

Это методы и они тратят ресурсы, место этого мы определили их уровни:
- INFO
- ERROR

Потому как это КОНСТАНТЫ!
```python
level = logging.INFO if flag else logging.ERROR 
```
Используем переменную, что бы определить уровень, далее в методе log.log используем её. 
```log.log(level, message, *args)``` — универсальный метод логирования, 
ты можешь заранее подготовить сообщение и просто вызывать log(...) с нужным уровнем.
Также мы используем форматирование строки через %s потому как f-строки в логах иногда могут обрабатывать ресурсы, 
которые обрабатывать не имеет смысла, например если не подходящий уровень. 
И обработка значений у нас теперь не ```round(delta, 1)```, а обработка идёт в самом сообщение логера через %.1f.

%.1f — стандартное C-подобное форматирование, которое не будет выполняться, 
если уровень логирования ниже (в отличие от f-строк).

