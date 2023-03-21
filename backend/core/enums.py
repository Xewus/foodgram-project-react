"""Настройки параметров.
"""
from enum import Enum, IntEnum


class Tuples(tuple, Enum):
    # Размер сохраняемого изображения рецепта
    RECIPE_IMAGE_SIZE = 500, 300
    # Поиск объектов только с переданным параметром.
    # Например только в избранном: `is_favorited=1`
    SYMBOL_TRUE_SEARCH = '1', 'true'
    # Поиск объектов не содержащих переданный параметр.
    # Например только не избранное: `is_favorited=0`
    SYMBOL_FALSE_SEARCH = '0', 'false'
    ADD_METHODS = 'GET', 'POST'
    DEL_METHODS = 'DELETE',
    ACTION_METHODS = 'GET', 'POST', 'DELETE'
    UPDATE_METHODS = 'PUT', 'PATCH'


class Limits(IntEnum):
    # Максимальная длина email (User)
    MAX_LEN_EMAIL_FIELD = 256
    # Максимальная длина строковых полей моделей в приложении "users"
    MAX_LEN_USERS_CHARFIELD = 32
    # Минимальная длина юзернейма (User)
    MIN_LEN_USERNAME = 3
    # Максимальная длина строковых полей моделей в приложении "recipes"
    MAX_LEN_RECIPES_CHARFIELD = 64
    # Максимальная длина единицы измеренияs моделей в приложении "recipes"
    MAX_LEN_MEASUREMENT = 256
    # Максимальная длина текстовых полей моделей в приложении "recipes"
    MAX_LEN_RECIPES_TEXTFIELD = 5000
    # Минимальное время приготовления рецепта в минутах
    MIN_COOKING_TIME = 1
    # Максимальное время приготовления рецепта в минутах
    MAX_COOKING_TIME = 300
    # Минимальное количество ингридиентов для рецепта
    MIN_AMOUNT_INGREDIENTS = 1
    # Максимальное количество ингридиентов для рецепта
    MAX_AMOUNT_INGREDIENTS = 32


class UrlQueries(str, Enum):
    # Параметр для поиска ингридиентов по вхождению значения в название
    SEARCH_ING_NAME = 'name'
    # Параметр для поиска объектов в списке "избранное"
    FAVORITE = 'is_favorited'
    # Параметр для поиска объектов в списке "покупки"
    SHOP_CART = 'is_in_shopping_cart'
    # Параметр для поиска объектов по автору
    AUTHOR = 'author'
    # Параметр для поиска объектов по тэгам
    TAGS = 'tags'
