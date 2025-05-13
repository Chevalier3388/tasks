"""
Что должен понимать разработчик на 3-ом уровне(middle+):
1. Понимать архитектурные различия между asyncio, Trio, uvloop, gevent.
2. Уметь оценивать, когда и какую реализацию целесообразно применять.
3. Знать, какие библиотеки совместимы с каждой моделью (например, не все asyncio-библиотеки работают в Trio).
4. Уметь писать простые примеры на разных фреймворках.
5. Понимать понятия "structured concurrency", "greenlet", "drop-in replacement".
6. Учитывать производительность, читаемость, дебаггинг и экосистему при выборе.
"""


print("asyncio")
"""
Стандартная библиотека Python.
Использует event loop, корутины, задачи (Task), Future.
Поддерживается официально, огромная экосистема.
Structured concurrency реализован только частично (TaskGroup с Python 3.11+).
"""
import asyncio

async def work_a(name):
    await asyncio.sleep(1)
    print(f"{name} done")

async def main():
    await asyncio.gather(work_a("A"), work_a("B"))

asyncio.run(main())

print("trio")
"""
Альтернатива с фокусом на structured concurrency.
Нет "голых" Task, всё выполняется строго в рамках nursery.
Лучше защищает от утечек задач и race conditions.
Меньше экосистема, но отличная читаемость и отладка.
"""
import trio

async def work_t(name):
    await trio.sleep(1)
    print(f"{name} done")

async def main():
    async with trio.open_nursery() as nursery:
        nursery.start_soon(work_t, "A")
        nursery.start_soon(work_t, "B")

trio.run(main)

print("uvloop")
"""
Быстрый event loop, реализованный на Cython (на базе libuv — та же основа, что и у Node.js).
Полностью совместим с asyncio: drop-in replacement.
Используется для ускорения сетевых приложений.
Меняет только внутренности event loop'а, API тот же.
"""

import asyncio
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def work_u(name):
    await asyncio.sleep(1)
    print(f"{name} done")

async def main():
    await asyncio.gather(work_u("A"), work_u("B"))

asyncio.run(main())

print("Gevent")

"""
Основан на greenlet'ах — микропотоках (green threads).
Использует монкипатчинг стандартных библиотек (socket, ssl, threading, и т.д.).
Можно писать "синхронный" код, который работает асинхронно.
Очень простой вход, но слабый контроль над concurrency.
Совместим только с экосистемой Gevent.

✅ Когда выбрать gevent:
У тебя старый код с requests, psycopg2, socket, и ты не хочешь переписывать его на asyncio.
Ты пишешь простой сервер, где проще использовать синхронный стиль, но нужен async-профит.
❌ Когда не стоит:
Современные async-фреймворки (FastAPI, AIOHTTP, SQLModel и т.п.).
Тебе важна прозрачность и контроль, а не implicit monkey-patching.
"""

import gevent
from gevent import monkey
monkey.patch_all()

import time

def work_g(name):
    time.sleep(1)
    print(f"{name} done")

g1 = gevent.spawn(work_g, "A")
g2 = gevent.spawn(work_g, "B")
gevent.joinall([g1, g2])


import requests

monkey.patch_all()

def download(url):
    print(f"Start {url}")
    response = requests.get(url)
    print(f"Done {url}: {len(response.content)} bytes")

start = time.time()
gevent.joinall([
    gevent.spawn(download, 'https://httpbin.org/delay/1'),
    gevent.spawn(download, 'https://httpbin.org/delay/1'),
])
print(f"Took: {time.time() - start:.2f} sec")



"""
Вопрос:
Что такое uvloop, и почему его называют drop-in replacement для asyncio?

Ответ:
uvloop — это высокопроизводительный ивент-луп, написанный на Cython 
и использующий libuv (тот же движок, что и в Node.js). Он реализует тот же интерфейс, 
что и стандартный event loop asyncio, поэтому ты можешь просто заменить его одной строкой:

import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
Называется drop-in потому что он полностью совместим с API asyncio, 
и его можно «вставить» без переписывания остального кода.

uvloop значительно быстрее стандартного event loop (в некоторых задачах в 2-4 раза), 
особенно при большом количестве соединений или операций с сетью.

Вопрос:
Чем отличается модель конкурентности в Trio от asyncio, и почему Trio считается «более безопасным»?

Ответ:
Structured Concurrency
В Trio параллельные задачи всегда создаются внутри «детского сада» (nursery), 
и они автоматически управляются вместе: когда ты выходишь из nursery, все дочерние задачи уже завершены или отменены. 
В asyncio до Python 3.11 задачи часто «убегали в фон», 
если ты забыл их await-ить, что приводило к утечкам и неконтролируемым исключениям.

Безопасность отмены
В Trio отмена всегда явная и происходит через контекст nursery.cancel_scope, где ты чётко управляешь, 
какие задачи будут отменены и когда. В asyncio задача могла быть случайно отменена извне и скрыть ошибки, 
если ты не ловил CancelledError.

Единый стиль API
В Trio нет множества точек входа 
(create_task, gather, as_completed, ensure_future и т.д.). 
Есть только nursery.start_soon и понятная модель: это упрощает отладку и чтение кода.

Управление ресурсами
Trio поощряет пиcать код так, чтобы все ресурсы (сокеты, файлы, блокировки) 
освобождались автоматически при выходе из контекста, благодаря async with и nursery, 
тогда как в asyncio можно было забыть закрыть и оставить висящие дескрипторы.

Вопрос:
Как в коде на asyncio ты переключаешься на использование uvloop? Покажи пример.

Ответ:


import asyncio
import uvloop

# Устанавливаем uvloop как стандартный event loop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

async def main():
    await asyncio.sleep(1)
    print("Привет из uvloop!")

asyncio.run(main())


uvloop — это drop-in замена стандартному asyncio loop на базе Cython и libuv.
Совместим со всем API asyncio, но значительно быстрее (в некоторых задачах x2–x4).
Примерно с Python 3.12/3.13 (особенно на Linux), 
стандартный asyncio уже почти догнал uvloop, 
поэтому выигрыш от uvloop есть, но не такой драматичный.

Нюансы:
uvloop не кроссплатформен: он работает только на Unix (Linux/macOS).
Он не улучшит производительность, если у тебя блокирующий код внутри async def.
Ты не можешь использовать его в Pyodide или внутри некоторых embedded окружений.
"""