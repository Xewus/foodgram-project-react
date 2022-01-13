from string import hexdigits

from recipes.models import AmountIngredient

from rest_framework.serializers import ValidationError


def set_amount_ingredients(recipe, ingredients):
    """
    Записывает ингредиенты вложенные в рецепт.
    """
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )


def check_value_validate(value, klass=None):
    """
    Проверяет корректность переданного значения.
    При необходимости проверяет существует ли объект с переданным obj_id
    При нахождении объекта создаётся Queryset[],
    для дальнейшей работы возвращается первое (и единственное) значение.
    """
    if not str(value).isdecimal():
        raise ValidationError(
            f'{value} должно содержать цифру'
        )
    if klass:
        obj = klass.objects.filter(id=value)
        if not obj:
            raise ValidationError(
                f'{value} не существует'
            )
        return obj[0]


def is_hex_color(value):
    """
    Проверяет - может ли значение быть шестнадцатеричным цветом.
    """
    if len(value) not in (3, 6):
        raise ValidationError(
            f'{value} не правильной длины для цвета({len(value)}).'
        )
    if not set(value).issubset(hexdigits):
        raise ValidationError(
            f'{value} не шестнадцатиричное.'
        )


incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджЭячсмитьбю.'
)
