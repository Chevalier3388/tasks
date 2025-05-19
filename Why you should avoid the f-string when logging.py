"""
В logging лучше избегать f-строк ввиду их механики работы, сейчас поясню на примерах.
"""

import logging
import time

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def heavy_func():
    time.sleep(0.001)
    return 1


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        delta = time.perf_counter() - start
        print(f"Выполнение функции {func.__name__} заняло: {delta:.6f}")
        return result

    return wrapper


# f-строка
@timer
def f_string(value_for_log):
    for _ in range(100):
        logger.debug(f"Значение: {value_for_log()}")


# строка формата
@timer
def no_f_string(value_for_log):
    for _ in range(100):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Значение: %s", value_for_log())


if __name__ == "__main__":
    f_string(heavy_func)
    no_f_string(heavy_func)


"""
1) Вызов значения heavy_func — происходит немедленно, прямо при построении f-строки.
2) Подстановка в строку: результат функции вставляется в строку.
3) Формирование итоговой строки: создаётся готовая строка (Значение: 1)
4) Передача в логгер: эта уже готовая строка передаётся в logger.debug(...)
5) Проверка уровня логирования: 
- Если уровень ниже (DEBUG не активен), то строка не выводится.
- Но вся работа уже проделана — вычисление и форматирование.

🎯 Вывод:
Даже если сообщение не попадёт в лог, все вычисления и построение строки всё равно произойдут. 
Это нерационально при дорогих операциях.
"""

"""
1) Вызов logger.debug(...) с шаблоном и аргументами: 
- Шаблон: "Значение: %s" 
- Аргумент: value_for_log() (но ещё не вызывается).
2)Внутри логгера происходит: Сначала проверка: logger.isEnabledFor(logging.DEBUG)
3) Если уровень DEBUG отключён:
- Логгер просто возвращается сразу — ничего не делает.
- value_for_log() не вызывается.
- Формирование строки тоже не начинается.
Если уровень DEBUG включён:
- Тогда функция вызывается
- Строка формируется
- Сообщение выводится

🎯 Вывод:
Если лог не должен быть выведен — то и значения не будут вычислены, и строка не будет построена. 
Это делает данный способ максимально эффективным.
"""
