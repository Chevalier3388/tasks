# Тестирование асинхронного кода.

### 1. Основы тестирования
- Установка pytest-asyncio
```shell
  pip install pytest-asyncio
```
- Пример асинхронной функции для тестирования
```python
# async_operations.py
import asyncio

async def fetch_data(delay: float) -> str:
    await asyncio.sleep(delay)
    return "Данные получены"
```
- Тест с pytest-asyncio
```python
# test_async.py
import pytest
from async_operations import fetch_data

@pytest.mark.asyncio  # Важно: маркировка теста как асинхронного
async def test_fetch_data():
    result = await fetch_data(0.1)
    assert result == "Данные получены"
```
- Запуск:
```shell
  pytest test_async.py -v
```
### 2. Тестирование исключений в асинхронном коде
Асинхронная функция с исключением
```python
async def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Деление на ноль")
    await asyncio.sleep(0.1)
    return a / b
```
Проверка через pytest.raises
```python
@pytest.mark.asyncio
async def test_divide_by_zero():
    with pytest.raises(ValueError, match="Деление на ноль"):
        await divide(10, 0)
```
### 3. Фикстуры (fixtures) для асинхронного кода
Асинхронная фикстура
```python
@pytest.fixture
async def async_fixture():
    await asyncio.sleep(0.1)
    return 42

@pytest.mark.asyncio
async def test_with_async_fixture(async_fixture):
    assert async_fixture == 42
```
Фикстура с setup/teardown
```python
@pytest.fixture
async def database_connection():
    conn = await connect_to_db()  # Имитация подключения
    yield conn
    await conn.close()  # Очистка после теста

@pytest.mark.asyncio
async def test_db_query(database_connection):
    result = await database_connection.fetch("SELECT 1")
    assert result is not None
```
### 4. Параметризация асинхронных тестов
```python
@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (20, 4, 5),
])
@pytest.mark.asyncio
async def test_async_parametrize(a, b, expected):
    result = await divide(a, b)
    assert result == expected
```
### 5. Мокирование асинхронных зависимостей
Использование unittest.mock или pytest-mock
```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_mocked_async_call():
    mock = AsyncMock(return_value="Моковые данные")
    result = await mock()
    assert result == "Моковые данные"
    mock.assert_awaited_once()  # Проверка, что мок был вызван
```
Пример с мокированием HTTP-запроса
```python
import aiohttp
from unittest.mock import patch

@pytest.mark.asyncio
async def test_fetch_from_api():
    mock_response = {"key": "value"}
    
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)
        
        async with aiohttp.ClientSession() as session:
            response = await session.get("http://fake-api.com/data")
            data = await response.json()
            assert data == mock_response
```
### 6. Тестирование всего приложения (FastAPI пример)
Установка зависимостей
```shell
    pip install fastapi httpx pytest-asyncio
```
Тест API-эндпоинта
```python
from fastapi import FastAPI
from httpx import AsyncClient

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@pytest.mark.asyncio
async def test_fastapi_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
```
### 7. Проблемы и решения
Типичные ошибки:
- Забыли @pytest.mark.asyncio
→ Тест не будет работать, так как pytest не знает, как его запустить.
- Использование синхронных фикстур с асинхронным кодом
→ Фикстура должна быть async, если внутри есть await.
- Неправильное мокирование
→ Для асинхронных методов используйте AsyncMock, а не обычный Mock.

Оптимизация скорости^
- Используйте asyncio.sleep(0) вместо реальных задержек в тестах.
- Запускайте тесты параллельно с pytest-xdist:
```shell
  pip install pytest-xdist
  pytest -n 4  # 4 потока
```
***pytest-xdist*** — это плагин для фреймворка pytest, который позволяет запускать тесты параллельно на нескольких ядрах процессора или машинах.
### Главное:

- Всегда маркируйте тесты как `````@pytest.mark.asyncio.`````
- Для мокирования используйте AsyncMock.
- Тестируйте не только успешные сценарии, но и ошибки.
- Примеры выше покрывают 95% повседневных задач. Для сложных кейсов (например, тестирование WebSocket) можно использовать библиотеки вроде websockets или asgi-lifespan.