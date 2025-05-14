"""
Что должен понимать разработчик на 2-ом уровне(middle):
1. Как работает асинхронный ввод/вывод независимо от языка.
2. Concurrency vs Parallelism разработчик должен уметь различать два подхода.
3. Task, Future, CancelledError, TaskGroup, разработчик должен понимать, как работать с объектами Task и Future,
как обрабатывать ошибки через CancelledError,
и как использовать TaskGroup для управления групповыми задачами.
4. gather, chain, cancel, join, is_coroutine разработчик должен знать и уметь использовать функции и методы.
"""
from asyncio import CancelledError

"""
1. Асинхронный ввод.вывод - это модель программирования, 
которая позволяет выполнять несколько задач одновременно не блокируя выполнение программы.
Эта модель полезна, когда нужно обрабатывать множество I/O задач(работа с файлами, сетью, базами данных)
"""

"""
2. Concurrency vs Parallelism:
Concurrency — несколько задач выполняются, переключаясь между собой (например, с помощью async/await в Python).
Parallelism — несколько задач выполняются действительно параллельно на разных процессах или ядрах процессора.

Важно понимать, что concurrency не обязательно подразумевает реальное одновременное выполнение, 
а parallelism — реальную параллельность.
"""

"""
3. Task — объект, который представляет выполнение корутины в будущем. 
Ты можешь использовать asyncio.create_task() для создания Task-ов.
Future — объект, который представляет результат выполнения корутины или другой асинхронной задачи в будущем.
CancelledError — ошибка, которая возникает, когда задача или корутина отменяется.
TaskGroup — группа задач, которая позволяет управлять несколькими задачами одновременно.
"""
# Task
import asyncio

print("Task")
async def say_hello_t(name):
    await asyncio.sleep(1)
    return f"Hello, {name}"

async def main():
    task = asyncio.create_task(say_hello_t("Alice"))  # создаём Task
    print(f"task: {task}")
    result = await task  # дожидаемся завершения задачи
    print(result)

asyncio.run(main())
"""
asyncio.create_task() создаёт задачу (Task), которая выполнится в будущем.
После этого мы используем await для получения результата задачи, когда она завершится.
"""

# Future
print("Future")
async def say_hello_f(name, future):
    await asyncio.sleep(1)
    future.set_result(f"Hello, {name}")  # устанавливаем результат в future

async def main():
    loop = asyncio.get_event_loop()
    future = loop.create_future()  # создаём Future
    print(f"future: {future}")
    await say_hello_f("Bob", future)
    print(future.result())  # выводим результат из Future

asyncio.run(main())
"""
Мы создаём Future с помощью loop.create_future().
В корутине мы устанавливаем результат в Future с помощью future.set_result(), 
и позже мы получаем результат через future.result().
"""


# TaskGroup
print("TaskGroup")
async def say_hello_t_g(name):
    await asyncio.sleep(1)
    print(f"Hello, {name}")

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(say_hello_t_g("Alice"))
        tg.create_task(say_hello_t_g("Bob"))
    # После выхода из блока with, все задачи завершены.

asyncio.run(main())
"""
Мы используем async with asyncio.TaskGroup() для управления несколькими задачами.
Когда все задачи завершатся, программа продолжит выполнение.
"""



"""
4. gather — позволяет запускать несколько асинхронных задач одновременно и дождаться их завершения.
chain — позволяет объединить несколько асинхронных операций в одну цепочку.
cancel — отменяет выполнение задачи.
join — блокирует выполнение до завершения всех задач.
is_coroutine — проверяет, является ли объект корутиной.
"""
print("gather")
# gather
async def say_hello(name):
    await asyncio.sleep(1)
    print(f"Hello, {name}")

async def main():
    await asyncio.gather(
        say_hello("Alice"),
        say_hello("Bob"),
        say_hello("Charlie")
    )

asyncio.run(main())
"""
asyncio.gather() позволяет одновременно запускать несколько корутин.
В данном примере три задачи выполняются одновременно.
"""

# chain, cancel, join, is_coroutine
print("chain, cancel, join, is_coroutine")
async def task1():
    await asyncio.sleep(2)
    print("Task 1 completed")


async def task2():
    print("task2 стартовала")
    try:
        await asyncio.sleep(3)
        print("Task 2 finished")
    except asyncio.CancelledError:
        print("Task 2 была отменена внутри")
        await asyncio.sleep(0)
        raise  # важно пробросить дальше
    finally:
        await asyncio.sleep(0)
        print("Task 2 завершается (finally)")


"""
В Python asyncio.create_task(...) только регистрирует задачу в планировщике.
Если ты сразу вызываешь cancel(), то задача:
получает CancelledError, просто завершает своё выполнение с флагом cancelled
"""
async def main():

    task1_ = asyncio.create_task(task1())  # создаём задачу
    task2_ = asyncio.create_task(task2())  # создаём задачу

    await asyncio.sleep(0.1) # без этого таска даже не отобразится в
    # Пример использования cancel()
    task2_.cancel()  # отменяем task2

    # Пример использования join()
    await task1_  # ожидаем завершения task1
    try:
        await task2_
    except asyncio.CancelledError:
        print(f"Главный поток поймал отмену task2")

    # Пример использования is_coroutine()
    print(f"task1 is a coroutine: {asyncio.iscoroutine(task1)}")
    """
    print(f"task1 is a coroutine: {asyncio.iscoroutine(task1)}") вернёт False
    Потому что task1 — это ссылка на функцию, а не вызванная корутина. 
    Чтобы это было True, нужно передать вызов этой функции, например:
    asyncio.iscoroutine(task1())  # вот это вернёт True
    """

    # Пример использования chain (объединяем несколько асинхронных операций)
    async for result in asyncio.as_completed([task1_, task2_]):
        print(result)

asyncio.run(main())

"""
cancel() — отменяет выполнение task2.
join() — блокирует выполнение до завершения task1.
iscoroutine() — проверяет, является ли task1 корутиной.
chain — используется через asyncio.as_completed() для того, чтобы работать с несколькими асинхронными задачами, как с цепочкой.
"""


"""
Отдельно разобрать cancel()
"""
print("Отдельно разобрать cancel()")

async def my_task():
    print("START task")  # <- не будет вызвано, если cancel сработает до запуска
    try:
        print("TRY")
        await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("CANCELLED")
        raise
    finally:
        print("FINALLY")

async def main():
    task = asyncio.create_task(my_task())
    await asyncio.sleep(0.1)  # даём loop'у шанс запустить задачу
    task.cancel()  # отмена сразу после создания
    # await asyncio.sleep(0.1)

    try:
        await task
    except asyncio.CancelledError:
        print("MAIN caught cancellation")

asyncio.run(main())
"""
Вывод будет:
Отдельно разобрать cancel()
START task
TRY
CANCELLED
FINALLY
MAIN caught cancellation

но если:
await asyncio.sleep(0.1)  # даём loop'у шанс запустить задачу
    task.cancel()  # отмена сразу после создания
поменять местами вывод будет:
MAIN caught cancellation
"""

"""
1. Когда корутина будет вызвана в Python с использованием asyncio.create_task()?
Ответ:
Корутина, переданная в asyncio.create_task(), не будет немедленно выполняться. 
Она будет зарегистрирована в event loop и начнёт исполняться при следующем шаге loop'а, 
или когда вы используете await на задаче. 
Это позволяет эффективно планировать задачи и выполнять их в подходящий момент.

2. Что происходит с корутиной, когда она зарегистрирована в event loop, но ещё не начала выполняться?
Ответ:
Когда корутина создаётся с помощью asyncio.create_task(), 
она просто добавляется в очередь задач event loop. 
Она будет ждать своего времени для выполнения, пока event loop не начнёт её процессинг, 
например, при следующем цикле или при вызове await на задаче.

3. Что происходит, если корутина ещё не началась выполнять свой код, но ей назначена отмена через task.cancel()?
Ответ:
Корутина не сразу отменяется. Если отмена происходит до того, 
как задача начнёт выполнение (то есть до первого шага в event loop), 
то она просто завершится с CancelledError, и исключение будет выброшено в тот момент, 
когда эта корутина начнёт своё выполнение в event loop.

4. Когда отмена задачи реально влияет на её выполнение?
Ответ:
Отмена задачи через task.cancel() будет фактически осуществляться в тот момент, 
когда задача начнёт выполняться. Корутина получает CancelledError в том месте, 
где она начинает своё выполнение. Это важно, потому что до начала работы корутина не знает о том, 
что она была отменена.

5. Что происходит, когда вызывается task.cancel()?
Ответ:
Метод task.cancel() не завершает задачу мгновенно, 
а лишь помечает её как отменённую, установив флаг в объекте задачи. 
Само исключение CancelledError будет выброшено только когда выполнение задачи действительно начнётся в event loop. 
Если в этот момент задача ещё не выполнялась, она будет отменена в момент её старта.

6. Что происходит, если задача отменена, но она ещё не была вызвана через await?
Ответ:
Если задача была отменена, но её выполнение ещё не началось (то есть вы не вызвали await), 
она просто завершится с исключением CancelledError. Важно, что задача не будет зафиксирована в try/except, 
так как исключение не будет выброшено до того момента, как корутина начнёт работать.

7. Попадает ли исключение CancelledError в блок try/except, если задача отменена до выполнения?
Ответ:
Нет, если задача была отменена до того, как корутина начала своё выполнение (и, следовательно, до входа в блок try), 
исключение CancelledError не попадёт в try/except. Исключение будет выброшено только тогда, 
когда корутина начнёт выполняться в event loop.

8. Как гарантировать, что задача будет обработана с использованием await после её создания?
Ответ:
Для того чтобы задача начала своё выполнение и могла быть обработана, 
необходимо использовать await. await активирует выполнение корутины и передаёт управление в event loop. 
Это важно для того, чтобы задачу можно было отслеживать и взаимодействовать с ней.

9. Почему иногда задача не выполняется сразу после её создания?
Ответ:
Задача может не начать выполняться сразу, 
потому что event loop может ещё не был готов выполнить её, 
либо другие задачи уже находятся в очереди. 
В случае высокой нагрузки или при наличии множества задач в очереди event loop, 
задача может не получить исполнения сразу, и на это может потребоваться некоторое время.

10. Что происходит, если задача начинает выполняться, но её выполнение прерывается из-за отмены?
Ответ:
Если задача была отменена в процессе выполнения, 
то в момент её работы будет выброшено исключение CancelledError. 
Это исключение можно перехватить внутри самой задачи в блоке except, 
если требуется выполнить какую-то очистку или логирование, прежде чем задача завершится.
"""