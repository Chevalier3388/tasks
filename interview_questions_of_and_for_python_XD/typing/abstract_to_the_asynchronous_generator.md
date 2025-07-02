# AsyncGenerator[YieldType, SendType] — типизация асинхронных генераторов

Асинхронные генераторы (async def + yield) используются для:
- Потоковой обработки данных (например, чтение файлов, запросов к API).
- Работы с очередями (RabbitMQ, Kafka).
- Стриминга в веб-фреймворках (FastAPI, Django).
Типизация помогает:
- Чётко указать, какие данные генерируются (YieldType).
- Запретить/разрешить передачу данных в генератор (SendType).
## Разбираем параметры
### ```YieldType``` — что возвращает ```yield```
```python
from typing import AsyncGenerator
import asyncio

async def countdown(n: int) -> AsyncGenerator[int, None]:
    while n > 0:
        yield n
        await asyncio.sleep(1)
        n -= 1

# Асинхронная функция для запуска
async def main():
    async for num in countdown(3):  # num — int
        print(num)  # Выведет 3, 2, 1 с интервалом в 1 секунду

# Запуск асинхронного кода
asyncio.run(main())
```
Что будет без типизации?
IDE и mypy не поймут, что num — это int.
### SendType — что можно передать в генератор через .asend()
```python
from typing import AsyncGenerator
import asyncio


async def chat_bot() -> AsyncGenerator[str, str]:
    """Асинхронный генератор для чат-бота с двусторонней коммуникацией."""
    try:
        # Первое сообщение от бота
        response = yield "Привет! Как дела?"
        
        while True:
            # Проверка команды завершения
            if any(word in response.lower() for word in ["пока", "выход", "завершить", "стоп", "exit", "stop"]):
                yield "До свидания! Было приятно пообщаться."
                break
                
            # Эхо-ответ с анализом сообщения
            if "?" in response:
                response = yield "Интересный вопрос! Давайте обсудим."
            else:
                response = yield f"Вы сказали: '{response}'. Продолжайте!"
                
    finally:
        print("\nБот: Соединение закрыто.")


async def main():
    """Пример использования чат-бота."""
    bot = chat_bot()
    
    try:
        # Инициализация
        greeting = await anext(bot)
        print(f"Бот: {greeting}")
        
        # Основной цикл диалога
        while True:
            user_input = input("Вы: ")
            response = await bot.asend(user_input)
            print(f"Бот: {response}")
            
    except StopAsyncIteration:
        print("\nДиалог завершен.")
    finally:
        print("Сессия окончена.")


if __name__ == "__main__":
    asyncio.run(main())
```
## Важные нюансы
### Нет ReturnType
В отличие от Generator, асинхронный генератор не может вернуть значение через return.


### Асинхронные генераторы незаменимы для:
- Работы с потоками данных
- Постепенной обработки
- Сценариев "запрос-ответ-ожидание"
- Ресурсоёмких операций

Они дополняют обычные асинхронные функции, а не заменяют их. В современных приложениях часто используют оба подхода вместе.