# Сигнатура функции
Сигнатура функции Сигнатура — это её "паспорт", который определяет:
- Имя функции
- Параметры (их количество, типы, порядок)
- Возвращаемый тип

```python
def greet(name: str, age: int) -> str:
    return f"Привет, {name}! Тебе {age} лет."
```
Сигнатура: ```greet(name: str, age: int) -> str```

Что бы изменить сигнатуру функции через декоратор, сохранить типы. 
Можно использовать ParamSpec для захвата исходных параметров и Concatenate для добавления новых.