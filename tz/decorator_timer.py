"""
Написать реализацию декоратора для измерения и логирования времени работы произвольной функции. Декоратор не должен изменять поведение функции.
В примере представлена функция f для которой нужно реализовать декоратор timeit, а ниже даны примеры результатов логирования после вызова функции.

f(1)
[INFO] f(1): 1.1 sec


f('1')
[ERROR] f('1'): 0.1 sec
"""

from functools import wraps
import logging
import time

logging.basicConfig(level=logging.INFO, format="[%(levelname)s], %(message)s")
logger = logging.getLogger("my_loger")


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
                level = logging.INFO if flag else logging.ERROR
                # Чем проще объект, которым мы оперируем — тем легче с ним работать, меньше багов, выше переносимость.
                # Даже если в лоб оба подхода дают тот же результат —
                # log_level предпочтительнее как более универсальный и безопасный путь.
                # По сравнению с log_method = log.info if flag else log.error
                log.log(level, "%s(%s) %.1f sec", func.__name__, params_func, delta)
                # log.log(...) — универсальный способ логирования с переменным уровнем.
                # Вместо вызова конкретного метода (info(), warning()) ты вызываешь один метод,
                # передавая уровень как аргумент.
                # Это делает код более гибким и масштабируемым, особенно в сложных системах или библиотеках.

        return inner

    return wrapper


@timeit(logger)
def f(s):
    time.sleep(s)
    return 5


def main():
    value = f(1)
    print(value)
    try:
        f("1")
    except TypeError:
        print("Task failed successfully")
    try:
        f(1, a=3, x="a", y="3")
    except TypeError:
        print("Task failed successfully")


if __name__ == "__main__":
    main()
