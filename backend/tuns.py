# HTTP методы разрешённые для добавления объектов
ADD_METHODS = ('GET', 'POST',)

# HTTP методы разрешённые для удаления объектов
DEL_METHODS = ('DELETE',)

# HTTP методы разрешённые для изменения объектов
UPDATE_METHODS = ('PUT', 'PATCH')

# Символы, передаваемын в URL для активации фильтров поиска
SYMBOL_FOR_SEARCH = ('1', 'true',)

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
