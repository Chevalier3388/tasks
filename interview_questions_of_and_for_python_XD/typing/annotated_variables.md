## Базовые аннотации
```python
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old."
```
### ```int``` – целое число
```python
x: int = 42
```
### ```str``` – строка
```python
name: str = "Alice"
```
### ```float``` – число с плавающей запятой
```python
pi: float = 3.14
```
### ```bool``` – логическое значение (```True```/```False```)
```python
is_active: bool = True
```
### ```list``` – список (можно уточнить тип элементов)
```python
numbers: list[int] = [1, 2, 3]
words: list[str] = ["hello", "world"]
```
### ```tuple``` – кортеж (можно указать типы элементов по порядку)
```python
point: tuple[int, int] = (10, 20)
mixed: tuple[str, int, bool] = ("text", 123, False)
```
### ```dict``` – словарь (указываются типы ключей и значений)
```python
person: dict[str, str] = {"name": "Alice", "age": "30"}  # если age должен быть int, лучше использовать TypedDict
grades: dict[str, float] = {"math": 4.5, "physics": 5.0}
```
### ```set``` – множество (указывается тип элементов)
```python
unique_numbers: set[int] = {1, 2, 3}
```
### ```None``` – отсутствие значения (обычно для возвращаемых значений)
```python
def do_nothing() -> None:
    print("Nothing happens")
```