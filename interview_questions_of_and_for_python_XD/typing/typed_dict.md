# TypedDict
## TypedDict - мощный инструмент для явной типизации словарей.

TypedDict — это специальный тип в Python, 
который позволяет строго описывать структуру словаря (ключи и типы их значений). 
Он используется для статической проверки типов (например, через mypy или IDE), 
чтобы избежать ошибок при работе с данными в виде словарей.

TypedDict нужен, когда:
- Ваши данные — это словари (например, JSON из API, конфиги, данные из БД).
- Вы хотите явно указать, какие ключи допустимы и каких типов должны быть их значения.

```python
from typing import TypedDict

# Определяем структуру словаря
class User(TypedDict):
    id: int
    name: str
    email: str | None  # Поле может быть None
    is_active: bool

# Создаем словарь, соответствующий этой структуре
user_data: User = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": True
}
```
Что даёт ```TypedDict```:
- Проверка типов: user_data["id"] = "123". Будет подчеркивание, так как id должен быть int.
- Автодополнение в IDE (PyCharm, VSCode) при обращении к ключам.
- Документирование структуры данных прямо в коде.

### Параметр ```total```
Параметр ```total=False``` делает все поля необязательными.
###  Вложенные структуры
```python
from typing import TypedDict

# Определяем структуру словаря
class User(TypedDict, total=False):
    id: int
    name: str
    email: str | None  # Поле может быть None
    is_active: bool
    
class Address(TypedDict):
    city: str
    zip_code: str

class UserWithAddress(User):
    address: Address  # Добавляем вложенный словарь

user: UserWithAddress = {
    "id": 1,
    "name": "Alice",
    "is_active": True,
    "address": {
        "city": "Moscow",
        "zip_code": "123456"
    }
}
```
### Можно расширять существующие TypedDict:
```python
class AdminUser(User):
    permissions: list[str]

admin: AdminUser = {
    "id": 1,
    "name": "Admin",
    "is_active": True,
    "permissions": ["read", "write"]
}
```
TypedDict — это способ строго типизировать словари в Python. 
Он не влияет на выполнение кода, 
но помогает находить ошибки на этапе разработки через статическую проверку типов. 
Полезен для работы с JSON, API и конфигами.

- Только для статической проверки типов (в runtime это обычный dict).
- Нет валидации данных (в отличие от Pydantic или dataclasses).
- Pydantic — если нужна валидация данных в runtime.