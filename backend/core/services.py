"""Модуль вспомогательных функций.
"""
from recipes.models import AmountIngredient, Recipe


def recipe_amount_ingredients_set(
    recipe: Recipe,
    ingredients: list[dict]
) -> None:
    """Записывает ингредиенты вложенные в рецепт.

    Создаёт объект AmountIngredient связывающий объекты Recipe и
    Ingredient с указанием количества(`amount`) конкретного ингридиента.

    Args:
        recipe (Recipe):
            Рецепт, в который нужно добавить игридиенты.
        ingridients (list[dict]):
            Список ингридентов и количества сих.
    """
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )


# Словарь для сопостановления латинской и русской стандартных раскладок.
incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
