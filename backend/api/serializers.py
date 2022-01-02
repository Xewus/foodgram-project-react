from django.contrib.auth import get_user_model
from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, Tag
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        ValidationError)
from rest_framework.settings import api_settings

from .services import set_amount_ingredients
from .tuns import MAX_LEN_CHARFIELD, MIN_USERNAME_LENGTH

User = get_user_model()


class UserSerializer(ModelSerializer):
    '''
    Сериализатор для использования с моделью User,
    Создание пользователей разрешено с юзернеймами только из букв
    определённой в настройках длины.
    Метод "get_is_subscribed" определяет - подписан ли
    текущий пользователь на просматриваемого пользователя.
    '''
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
        read_only_fields = ('is_subscribed', )

    def get_is_subscribed(self, obj):
        '''
        Определяет - подписан ли текущий пользователь
        на просматриваемого пользователя.
        '''
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscribe.filter(id=obj.id).exists()

    def create(self, validated_data):
        '''
        Создаёт нового пользователя с запрошенными полями.
        '''
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
        '''
        Проверяет введённый юзернейм на соответствие
        установленным правилам.
        '''
        if len(username) < MIN_USERNAME_LENGTH:
            raise ValidationError(
                'Длина username допустима от '
                f'{MIN_USERNAME_LENGTH} до {MAX_LEN_CHARFIELD}'
            )
        if not username.isalpha():
            raise ValidationError(
                'В username допустимы только буквы.'
            )
        return username.capitalize()


class UserSubscribeSerializer(UserSerializer):
    '''
    Сериализатор для вывода авторов на которых подписан текущий пользователь.
    Метод "get_is_subscribed" переопределён, для уменьшения нагрузки,
    так как при вычислениях всё равно будет возвращать True.
    '''
    recipes = SerializerMethodField()
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
        '''
        Довольно странное поле по запросу фронтенда.
        '''
        return True

    def get_recipes(self, obj):
        '''
        Рецепты каждого автора с запрошенным лимитом.
        '''
        lim = (
            self.context['request'].query_params.get('recipes_limit')
        )
        if not lim:
            lim = api_settings.PAGE_SIZE
        lim = int(lim)
        return obj.recipes.values('id', 'name', 'image', 'cooking_time')[:lim]

    def get_recipes_count(self, obj):
        '''
        Показывает общее количество рецептов у каждого автора.
        '''
        return obj.recipes.count()


class TagSerializer(ModelSerializer):
    '''
    Сериализатор для вывода тэгов.
    '''
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )
        read_only_fields = '__all__',


class IngredientSerializer(ModelSerializer):
    '''
    Сериализатор для вывода ингридиентов.
    '''
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'measurement_unit',
        )
        read_only_fields = '__all__',


class RecipeSerializer(ModelSerializer):
    '''
    Сериализатор для работы с рецептами.
    '''
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
        '''
        Получает ингридиенты для каждого рецепта.
        '''
        ingredients = obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        '''
        Проверка - находится ли рецепт в избранном.
        '''
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        '''
        Проверка - находится ли рецепт в списке покупок.
        '''
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.carts.filter(id=obj.id).exists()

    def validate(self, data):
        name = str(self.initial_data.get('name')).strip()

        tags = self.initial_data.get('tags')
        if not isinstance(tags, list):
            raise ValidationError(
                '"tags" должен быть в формате "[]"'
            )
        for tag in tags:
            if not str(tag).isdigit():
                raise ValidationError(
                    'Ключ "tag" должен содержать цифру'
                )
            if not Tag.objects.filter(id=tag).exists():
                raise ValidationError(
                    'Такого тэга не существует'
                )

        ingredients = self.initial_data.get('ingredients')
        if not isinstance(ingredients, list):
            raise ValidationError(
                '"ingredients" должен быть в формате "[]"'
            )
        valid_ingredients = []
        for ing in ingredients:
            amount = str(ing.get('amount'))
            if not amount:
                raise ValidationError(
                    'Отсутствует ключ "amount'
                )
            if not str(amount).isdigit():
                raise ValidationError(
                    'Ключ "amount" должен содержать цифру'
                )
            id = ing.get('id')
            if not id:
                raise ValidationError(
                    'Отсутствует ключ "id'
                )
            if not str(id).isdigit():
                raise ValidationError(
                    'Ключ "id" должен содержать цифру'
                )
            ing = Ingredient.objects.filter(id=id)
            if not ing:
                raise ValidationError(
                    'Такого ингредиента не существует'
                )
            valid_ingredients.append(
                {'ing': ing[0], 'amount': amount})

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
        set_amount_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get(
            'tags', instance.tags)
        ingredients = validated_data.get(
            'ingredients', instance.ingredients)
        instance.image = validated_data.get(
            'image', instance.image)
        instance.name = validated_data.get(
            'name', instance.name)
        instance.text = validated_data.get(
            'text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)

        instance.tags.clear()
        instance.ingredients.clear()
        instance.save()
        instance.tags.set(tags)
        set_amount_ingredients(instance, ingredients)
        return instance


class AddDelSerializer(ModelSerializer):
    '''
    Сериализатор для добавления и удаления объектов
    по запросу с определённым URL.
    '''
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = '__all__',
