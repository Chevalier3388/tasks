

# 1. len(password) >= 10
# 2. "!@#$%*" in password
# 3. Заглавная бука in password
# 4. количество digits >= 3

from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")

class CustomValidationError(Exception):
    """Кастомное исключение для ошибок валидации"""
    def __init__(self, message, rule_name: str = None):
        self.message = message
        self.rule_name = rule_name or self.__class__.__name__
        super().__init__(message)

    def __str__(self):
        return f"{self.rule_name}: {self.message}"


class Rule(ABC):
    """Абстрактный базовый класс для правил валидации"""

    @abstractmethod
    def validate(self, *args, **kwargs) -> None:
        """
        Метод валидации значения.
        Если значение не проходит валидацию, выбрасывает CustomValidationError.
        """
        pass


class MinLengthRule(Rule):
    def __init__(self, min_len=10):
        self.min_len = min_len

    def validate(self, value: str):
        if len(value) < self.min_len:
            raise CustomValidationError(f"Должно быть > {self.min_len} символов!")

class HasSpecialCharRule(Rule):
    def __init__(self, chars="!@#$%*"):
        self.chars = chars

    def validate(self, value: str):
        if not any(char in self.chars for char in value):
            raise CustomValidationError(f"Нужен хотя бы 1 символ из {self.chars}")


class HasTitleRule(Rule):
    def validate(self, value: str):
        if not any(char.isupper() for char in value):  # Проверяем всю строку
            raise CustomValidationError("Нужна хотя бы 1 заглавная буква")

class MinDigitsRule(Rule):
    def __init__(self, need_digits):
        self._digits = need_digits


    def validate(self, value: str):
        if sum(c.isdigit() for c in value) < self._digits:
            raise CustomValidationError("Нужно минимум {} цифры".format(self._digits))  # Альтернативный вариант форматирования



class CustomValidator:
    """
    Класс для проверки валидности данных согласно разным правилам
    """
    def __init__(self):
        self._rules: list[Rule] = []

    def add_rule(self, rule: Rule):
        self._rules.append(rule)
        return self

    def checks(self, value: T) -> bool:
        """
        Проверяет значение по всем правилам.
        Возвращает True если все проверки прошли успешно.
        При первой же ошибке выбрасывает исключение CustomValidationError.
        """
        for rule in self._rules:
            rule.validate(value)
        return True



if __name__ == "__main__":
    l = MinLengthRule(10)
    h = HasSpecialCharRule()
    t = HasTitleRule()
    d = MinDigitsRule(3)

    my_valid = CustomValidator()
    my_valid.add_rule(l).add_rule(h).add_rule(t).add_rule(d)

    test_passwords = [
        "Aa12345!qwery",
        "short",
        "noSpecial123",
        "nocaps!123",
        "Aa!bcdefg"
    ]

    for password in test_passwords:
        try:
            my_valid.checks(password)
        except:
            print("{} not valid!".format(password))
        else:
            print("{} is valid!".format(password))
