# 23/02/2025 16/56
DATE_TIME_FORMAT = '%d/%m/%Y %H:%M'

"""
HTTP-методы для активации запросов.
"""
# HTTP методы разрешённые для добавления объектов
ADD_METHODS = ('GET', 'POST',)

# HTTP методы разрешённые для удаления объектов
DEL_METHODS = ('DELETE',)

# HTTP методы для @action разрешающие вход
# в метод для удаления и добавления объетов
ACTION_METHODS = [s.lower() for s in (ADD_METHODS + DEL_METHODS)]

# HTTP методы разрешённые для изменения объектов
UPDATE_METHODS = ('PUT', 'PATCH')

"""
URL-параметры для активации фильтров.
"""
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

# Поиск объектов только с переданным параметром
SYMBOL_TRUE_SEARCH = ('1', 'true',)

# Поиск объектов только без переданного параметра
SYMBOL_FALSE_SEARCH = ('0', 'false',)

"""
Литералы для выбора менеджера Мany-To-Many
в эндпоинтах обеспечивающих работу с этими менеджерами.
"""
# Создание "подписки". <user.subscribe>
SUBSCRIBE_M2M = 'subscribe'
# Добавление рецепта в "избранное". <user.favorites>
FAVORITE_M2M = 'favorite'
# Добавление рецепта в "список покупок". <user.carts>
SHOP_CART_M2M = 'shopping_cart'

"""
Настройки ограничений моделей.
"""
# Максимальная длина строковых полей моделей в приложении "users"
MAX_LEN_USERS_CHARFIELD = 150

# Минимальная длина юзернейма (User)
MIN_USERNAME_LENGTH = 3

# Максимальная длина email (User)
MAX_LEN_EMAIL_FIELD = 254

# Максимальная длина строковых полей моделей в приложении "recipes"
MAX_LEN_RECIPES_CHARFIELD = 200

# Максимальная длина текстовых полей моделей в приложении "recipes"
MAX_LEN_RECIPES_TEXTFIELD = 5000
