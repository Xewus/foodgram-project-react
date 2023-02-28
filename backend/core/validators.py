"""Модуль валидаторов.
"""
from re import compile
from string import hexdigits
from typing import TYPE_CHECKING, Union

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

if TYPE_CHECKING:
    from recipes.models import Ingredient, Tag


@deconstructible
class OneOfTwoValidator:
    """Проверяет введённую строку регулярными выражениями.

    Проверяет, соответствует ли введённая строка двум регулярным выражениям.
    Разрешенно не более, чем одно соответствие.
    Если регулярны выражения не переданы при вызове, применяет выражения
    по умолчанию. По умолчанию, во избежание коллизий,
    строка может быть только из латинских или только из русских букв.

    Attrs:
        first_regex (str):
            Первый вариант допустимого регулярного выражения для сравнения
            со значением. По умолчанию - только русские буквы.
        second_regex (str):
            Второй вариант допустимого регулярного выражения для сравнения
            со значением. По умолчанию - только латинские буквы.
        field (str):
            Название проверяемого поля.

        Raises:
            ValidationError:
                Переданное значение содержит символы разрешённые обоими
                регулярными выражениями.
    """
    first_regex = '[^а-яёА-ЯЁ]+'
    second_regex = '[^a-zA-Z]+'
    field = 'Переданное значение'
    message = '<%s> на разных языках либо содержит не только буквы.'

    def __init__(
        self,
        first_regex: str | None = None,
        second_regex: str | None = None,
        field: str | None = None,
    ) -> None:
        if first_regex is not None:
            self.first_regex = first_regex
        if second_regex is not None:
            self.second_regex = second_regex
        if field is not None:
            self.field = field
        self.message = f'\n{self.field} {self.message}\n'

        self.first_regex = compile(self.first_regex)
        self.second_regex = compile(self.second_regex)

    def __call__(self, value: str) -> None:
        if self.first_regex.search(value) and self.second_regex.search(value):
            raise ValidationError(self.message % value)


@deconstructible
class MinLenValidator:
    """Проверяет минимальную длину значения.

    Attrs:
        min_len (int):
            Минимально разрешённая длина значения.
            По умолчанию - `0`.
        field (str):
            Название проверямого поля.
        message (str):
            Сообщение, выводимое при передаче слишком короткого значения.

    Raises:
        ValidationError:
            Переданное значение слишком короткое.
    """
    min_len = 0
    field = 'Переданное значение'
    message = '\n%s недостаточной длины.\n'

    def __init__(
        self,
        min_len: int | None = None,
        field: str | None = None,
        message: str | None = None,
    ) -> None:
        if min_len is not None:
            self.min_len = min_len
        if field is not None:
            self.field = field
        if message is not None:
            self.message = message
        else:
            self.message = self.message % field

    def __call__(self, value: int) -> None:
        if len(value) < self.min_len:
            raise ValidationError(self.message)


def hex_color_validator(color: str) -> str:
    """Проверяет - может ли значение быть шестнадцатеричным цветом.

    Args:
        color (str):
            Значение переданное для проверки.

    Raises:
        ValidationError:
            Переданное значение не корректной длины.
        ValidationError:
            Символы значения выходят за пределы 16-ричной системы.
    """

    color = color.strip(' #')
    if len(color) not in (3, 6):
        raise ValidationError(
            f'Код цвета {color} не правильной длины ({len(color)}).'
        )
    if not set(color).issubset(hexdigits):
        raise ValidationError(
            f'{color} не шестнадцатиричное.'
        )
    if len(color) == 3:
        return f'#{color[0] * 2}{color[1] * 2}{color[2] * 2}'.upper()
    return '#' + color.upper()


def tags_exist_validator(tags_ids: list[int | str], Tag: 'Tag') -> None:
    """Проверяет наличие тэгов с указанными id.

    Args:
        tags_ids (list[int | str]): Список id.
        Tag (Tag): Модель тэгов во избежании цикличного импорта.

    Raises:
        ValidationError: Тэга с одним из указанных id не существует.
    """
    exists_tags = Tag.objects.filter(id__in=tags_ids)

    if len(exists_tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тэг')


def ingredients_exist_validator(
    ingredients: list[dict[str, str | int]],
    Ingredient: 'Ingredient'
) -> list[dict[str, Union[int, 'Ingredient']]]:
    """Проверяет список ингридиентов.

    Args:
        ingredients (list[dict[str, str  |  int]]):
            Список ингридиентов.
            Example: [{'amount': '5', 'id': 2073},]
        Ingredient (Ingredient):
            Модель ингридиентов во избежании цикличного импорта.

    Raises:
        ValidationError: Ошибка в переданном списке.

    Returns:
        list[dict[str, int | Ingridient]]: Проверенный список.
        Example: [{'amount': 5, 'ingredient': <Ingredient: шалфей г>},]
    """
    ings_ids = [None] * len(ingredients)

    for idx, ing in enumerate(ingredients):
        ingredients[idx]['amount'] = int(ingredients[idx]['amount'])
        if ingredients[idx]['amount'] < 1:
            raise ValidationError('Неправильное количество ингидиента')
        ings_ids[idx] = ing.pop('id', 0)

    ings_in_db = Ingredient.objects.filter(id__in=ings_ids).order_by('pk')
    ings_ids.sort()

    for idx, id in enumerate(ings_ids):
        ingredient: 'Ingredient' = ings_in_db[idx]
        if ingredient.id != id:
            raise ValidationError('Ингридент не существует')

        ingredients[idx]['ingredient'] = ingredient
    return ingredients
