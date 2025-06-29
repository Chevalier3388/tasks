## Проверка исключений в pytest
Для проверки исключений в тестах используется конструкция with pytest.raises(). Вот как это работает:
### Базовый синтаксис
```python
import pytest

def test_exception():
    with pytest.raises(ОжидаемоеИсключение):
        код_который_должен_вызвать_исключение()
```
### Пример с ValueError
Допустим, у нас есть функция, которая проверяет возраст:
```python
def validate_age(age):
    if age < 0:
        raise ValueError("Возраст не может быть отрицательным")
    return age
```
Тест для проверки исключения:
```python
def test_negative_age():
    with pytest.raises(ValueError):
        validate_age(-5)  # Должен вызвать ValueError
```
Проверка текста исключения:
```python
def test_negative_age_with_message():
    with pytest.raises(ValueError, match="не может быть отрицательным"):
        validate_age(-5)
```
- ```match``` принимает регулярное выражение или часть текста ошибки
Если нужно проверить атрибуты исключения:
```python
def test_negative_age_details():
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)
    
    assert "отрицательным" in str(exc_info.value)
```
```pytest.raises(ValueError)```
- Создает контекст, в котором мы ожидаем исключение ValueError
- Если исключение не возникнет — тест упадет

```as exc_info```
- Сохраняет информацию об исключении в переменную exc_info
- ```exc_info``` — это специальный объект с деталями исключения

```exc_info.value```
- Это само исключение (экземпляр ValueError)
- ```str(exc_info.value)``` дает доступ к тексту ошибки

Проверка текста
- ```assert "отрицательным" in str(exc_info.value)```
- Убеждаемся, что в сообщении об ошибке есть нужное слово

Можно проверять конкретные атрибуты исключения:

```python
class AgeError(ValueError):
    def __init__(self, age):
        self.age = age
        super().__init__(f"Invalid age: {age}")  # Вызов родительского конструктора

def test_custom_exception():
    with pytest.raises(AgeError) as exc_info:
        validate_age(-5)  # Предположим, что теперь вызывает AgeError
    assert exc_info.value.age == -5  # Проверяем кастомный атрибут
```
Вызов функции — для тестирования поведения кода
```python
class MyCustomError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(f"Error with code: {code}")  # Вызов родительского конструктора

def test_custom_exception():
    with pytest.raises(MyCustomError) as exc_info:
        raise MyCustomError(404)
    
    assert exc_info.value.code == 404
    assert str(exc_info.value) == "Error with code: 404"  # Теперь можно проверять и текст
```
raise в тестах — для тестирования исключений как объектов

### Когда использовать?
- Для проверки ошибочных сценариев
- Когда нужно убедиться, что функция вызывает исключение при неверных входных данных
- Для проверки типа и содержания исключений

Важные нюансы
- Тест провалится, если исключение не будет вызвано
- Можно проверять как встроенные исключения (ValueError, TypeError), так и пользовательские
- Для сложных проверок используйте exc_info.value чтобы получить доступ к объекту исключения

### Альтернатива в unittest
Если используете unittest, синтаксис немного отличается:
```python
import unittest

class TestValidation(unittest.TestCase):
    def test_negative_age(self):
        with self.assertRaises(ValueError):
            validate_age(-5)
```

