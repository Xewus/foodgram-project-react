from django.contrib.auth import get_user_model
from django.db.models import F

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Ingredient, Recipe, Tag

from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)

from .conf import MAX_LEN_USERS_CHARFIELD, MIN_USERNAME_LENGTH
from .services import (check_value_validate, is_hex_color,
                       instance_amount_ingredients_set)

User = get_user_model()


class ShortRecipeSerializer(ModelSerializer):
    """
    Сериализатор для модели Recipe
    с укороченным набором полей для некоторых эндпоинтов.
    """
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class UserSerializer(ModelSerializer):
    """
    Сериализатор для использования с моделью User,
    Создание пользователей разрешено с юзернеймами только из букв
    определённой в настройках длины.
    Метод "get_is_subscribed" определяет - подписан ли
    текущий пользователь на просматриваемого пользователя.
    """
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        """
        Определяет - подписан ли текущий пользователь
        на просматриваемого пользователя.
        """
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def create(self, validated_data):
        """
        Создаёт нового пользователя с запрошенными полями.
        """
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, username):
        """
        Проверяет введённый юзернейм на соответствие
        установленным правилам.
        """
        if len(username) < MIN_USERNAME_LENGTH:
            raise ValidationError(
                'Длина username допустима от '
                f'{MIN_USERNAME_LENGTH} до {MAX_LEN_USERS_CHARFIELD}'
            )
        if not username.isalpha():
            raise ValidationError(
                'В username допустимы только буквы.'
            )
        return username.capitalize()


class UserSubscribeSerializer(UserSerializer):
    """
    Сериализатор для вывода авторов на которых подписан текущий пользователь.
    Метод "get_is_subscribed" переопределён, для уменьшения нагрузки,
    так как при вычислениях с входными данными этого сериализатора
    всё равно будет возвращать True.
    """
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        """
        Cтранное поле по запросу фронтенда.
        """
        return True

    def get_recipes_count(self, obj):
        """
        Показывает общее количество рецептов у каждого автора.
        """
        return obj.recipes.count()


class TagSerializer(ModelSerializer):
    """
    Сериализатор для вывода тэгов.
    """
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = '__all__',

    def validate_color(self, color):
        """
        Проверяет и нормализует код цвета
        """
        color = str(color).strip(' #')
        is_hex_color(color)
        return color


class IngredientSerializer(ModelSerializer):
    """
    Сериализатор для вывода ингридиентов.
    """
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор для работы с рецептами.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = (
            'is_favorite',
            'is_shopping_cart',
        )

    def get_ingredients(self, obj):
        """
        Получает ингридиенты для каждого рецепта.
        """
        ingredients = obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        """
        Проверка - находится ли рецепт в избранном.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """
        Проверка - находится ли рецепт в списке покупок.
        """
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.carts.filter(id=obj.id).exists()

    def validate(self, data):
        name = str(self.initial_data.get('name')).strip()
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        values_as_list = (tags, ingredients)

        for value in values_as_list:
            if not isinstance(value, list):
                raise ValidationError(
                    f'"{value}" должен быть в формате "[]"'
                )

        for tag in tags:
            check_value_validate(tag, Tag)

        valid_ingredients = []
        for ing in ingredients:
            ing_id = ing.get('id')
            ingredient = check_value_validate(ing_id, Ingredient)

            amount = ing.get('amount')
            check_value_validate(amount)

            valid_ingredients.append(
                {'ingredient': ingredient, 'amount': amount}
            )

        data['name'] = name.capitalize()
        data['tags'] = tags
        data['ingredients'] = valid_ingredients
        data['author'] = self.context.get('request').user
        return data

    def create(self, validated_data):
        image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        instance_amount_ingredients_set(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.get(
            'tags', recipe.tags)
        ingredients = validated_data.get(
            'ingredients', recipe.ingredients)
        recipe.image = validated_data.get(
            'image', recipe.image)
        recipe.name = validated_data.get(
            'name', recipe.name)
        recipe.text = validated_data.get(
            'text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)

        recipe.tags.clear()
        recipe.ingredients.clear()
        recipe.save()
        recipe.tags.set(tags)
        instance_amount_ingredients_set(recipe, ingredients)
        return recipe
