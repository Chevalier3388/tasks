# Protocol в Python
Protocol — это способ сказать Python: 
"Вот какие методы и свойства должен иметь объект, 
чтобы работать в моей функции". 
При этом сам объект не обязан явно говорить, 
что он поддерживает этот Protocol.

Допустим, у нас есть функция, 
которая работает с объектами, у которых есть метод .draw():
```python
from typing import Protocol

# Определяем "интерфейс" — что должен уметь объект
class Drawable(Protocol):
    def draw(self) -> None:
        pass  # Тут просто указываем, что метод должен быть

# Класс, который НЕ наследует Drawable, но имеет нужный метод
class Circle:
    def draw(self):
        print("Рисую круг ⭕")

# Функция принимает любой объект с методом draw()
def render(obj: Drawable) -> None:
    obj.draw()

# Работает, хотя Circle не наследует Drawable!
circle = Circle()
render(circle)  # Выведет: "Рисую круг ⭕"
```
Зачем это нужно?
- Гибкость — классы не обязаны наследоваться от Protocol
- Ясность — сразу видно, какие методы нужны для работы
- Проверка типов — IDE подскажет, если объект не подходит
```python
from typing import Protocol, runtime_checkable

# Добавляем @runtime_checkable для проверки в runtime
@runtime_checkable
class Serializable(Protocol):
    def to_json(self) -> str:
        pass

class User:
    def to_json(self):
        return '{"name": "John"}'

def save(data: Serializable):
    if isinstance(data, Serializable):  # Проверяем, есть ли нужный метод
        print(data.to_json())

user = User()
save(user)  # Выведет: {"name": "John"}
```

Главные плюсы Protocol:
- Простота — не нужно наследоваться
- Гибкость — подходит любой объект с нужными методами
- Понятность — сразу видно, что требуется для работы