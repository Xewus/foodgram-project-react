"""Модуль валидаторов для пакета `users`.
"""
from re import compile

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class OneOfTwoValidator:
    """Проверяет введённую строку регулярными выражениями.

    Проверяет, соответствует ли введённая строка двум регулярным выражениям.
    Разрешенно не более, чем одно соответствие.
    Если регулярны выражения не переданы при вызове, применяет выражения
    по умолчанию. По умолчанию строка может быть только из латинских или
    только из русских букв.

    Args:
        first_regex(str):
            Первый вариант допустимого регулярного выражения для сравнения
            со значением. По умолчанию - только русские буквы.
        second_regex(str):
            Второй вариант допустимого регулярного выражения для сравнения
            со значением. По умолчанию - только латинские буквы.
        message(str):
            Сообщение, выводимое при передаче неправильного значения.

        Raises:
            ValidationError:
                Переданное значение содержит символы разрешённые обоими
                регулярными выражениями.
    """
    first_regex = '[^а-яёА-ЯЁ]+'
    second_regex = '[^a-zA-Z]+'
    message = (
        'Переданное значение на разных языках либо содержит что-то кроме букв.'
    )

    def __init__(self, first_regex=None, second_regex=None, message=None):
        if first_regex is not None:
            self.first_regex = first_regex
        if second_regex is not None:
            self.second_regex = second_regex
        if message is not None:
            self.message = message

        self.first_regex = compile(self.first_regex)
        self.second_regex = compile(self.second_regex)

    def __call__(self, value):
        if self.first_regex.search(value) and self.second_regex.search(value):
            raise ValidationError(self.message)


@deconstructible
class MinLenValidator:
    """Проверяет минимальную длину значения.

    Args:
        min_len(int):
            Минимально разрешённая длина значения.
            По умолчанию - `0`.
        message(str):
            Сообщение, выводимое при передаче слишком короткого значения.

    Raises:
        ValidationError:
            Переданное значение слишком короткое.
    """
    min_len = 0
    message = 'Переданное значение слишком короткое.'

    def __init__(self, min_len=None, message=None):
        if min_len is not None:
            self.min_len = min_len
        if message is not None:
            self.message = message

    def __call__(self, value):
        if len(value) < self.min_len:
            raise ValidationError(self.message)
