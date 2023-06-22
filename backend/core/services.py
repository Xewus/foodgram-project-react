"""Модуль вспомогательных функций.
"""
from datetime import datetime as dt
from typing import TYPE_CHECKING
from urllib.parse import unquote

from django.apps import apps
from django.db.models import F, Sum
from foodgram.settings import DATE_TIME_FORMAT
from recipes.models import AmountIngredient, Recipe

if TYPE_CHECKING:
    from recipes.models import Ingredient
    from users.models import MyUser


def recipe_ingredients_set(
    recipe: Recipe, ingredients: dict[int, tuple["Ingredient", int]]
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
    objs = []

    for ingredient, amount in ingredients.values():
        objs.append(
            AmountIngredient(
                recipe=recipe, ingredients=ingredient, amount=amount
            )
        )

    AmountIngredient.objects.bulk_create(objs)


def create_shoping_list(user: "MyUser") -> str:
    """Сфомировать список ингридкетов для покупки.

    Args:
        user (MyUser):
            Пользователь, для которго будет создаваться список.

    Returns:
        str:
            Список продуктов с указанием необходимого количества.
    """
    shopping_list = [
        f"Список покупок для:\n\n{user.first_name}\n"
        f"{dt.now().strftime(DATE_TIME_FORMAT)}\n"
    ]
    Ingredient = apps.get_model("recipes", "Ingredient")
    ingredients = (
        Ingredient.objects.filter(recipe__recipe__in_carts__user=user)
        .values("name", measurement=F("measurement_unit"))
        .annotate(amount=Sum("recipe__amount"))
    )
    ing_list = (
        f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
        for ing in ingredients
    )
    shopping_list.extend(ing_list)

    # ###########   Пример с использованием сырого SQL   ############ #
    # ingredients = Ingredient.objects.raw('''                        #
    # SELECT                                                          #
    #     ing.id,                                                     #
    #     ing.name AS name,                                           #
    #     ing.measurement_unit AS measurement,                        #
    #     SUM(ai.amount) AS amount                                    #
    # FROM recipes_ingredient AS ing                                  #
    # JOIN recipes_amountingredient AS ai ON ai.ingredients_id=ing.id #
    # JOIN recipes_recipe AS rcp ON ai.recipe_id=rcp.id               #
    # JOIN recipes_carts AS crt ON crt.recipe_id=rcp.id               #
    # WHERE crt.user_id=%s                                            #
    # GROUP BY ing.id, ing.name;                                      #
    # ''', (user.id,))                                                #
    #                                                                 #
    # for ing in ingredients:                                         #
    #     shopping_list.append(                                       #
    #         f'{ing.name}: {ing.amount} {ing.measurement}'           #
    #     )                                                           #
    ###################################################################

    shopping_list.append("\nПосчитано в Foodgram")
    return "\n".join(shopping_list)


def maybe_incorrect_layout(url_string: str) -> str:
    """Перевод слова, если пользователь не переключил раскладку.

    Args:
        url_string (str): Проверяемая строка.

    Returns:
        str: Проверенная строка.
    """
    equals = str.maketrans(
        "qwertyuiop[]asdfghjkl;'zxcvbnm,./",
        "йцукенгшщзхъфывапролджэячсмитьбю.",
    )
    if url_string.startswith("%"):
        return unquote(url_string).lower()

    return url_string.translate(equals).lower()
