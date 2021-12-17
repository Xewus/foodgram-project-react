from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (CASCADE, CharField, CheckConstraint,
                              DateTimeField, F, ForeignKey, ImageField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, Q, TextField,
                              UniqueConstraint)
from django.db.models.functions import Length
from django.forms import ValidationError

CharField.register_lookup(Length)

User = get_user_model()


def null_validator(value):
    if value < 1:
        raise ValidationError(
            ('%(value)s is not an even number'),
            params={'value': value},
        )


class Tag(Model):
    '''Тэги для рецептов.'''
    name = CharField(
        verbose_name='Тэг',
        max_length=200,
        unique=True,
    )
    color = CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        default='FF',
    )
    slug = CharField(
        verbose_name='Слаг тэга',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )
        constraints = (
            CheckConstraint(
                check=Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            CheckConstraint(
                check=Q(color__length__gt=0),
                name='\n%(app_label)s_%(class)s_color is empty\n',
            ),
            CheckConstraint(
                check=Q(slug__length__gt=0),
                name='\n%(app_label)s_%(class)s_slug is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name} (цвет: {self.color})'


class Ingredient(Model):
    '''Ингридиенты для рецептов'''
    MEASURES = [
        ('to taste', 'по вкусу'),
        ('gramm', 'г'),
        ('kilogramm', 'кг'),
        ('milliliter', 'мл'),
        ('liter', 'л'),
        ('teaspoon', 'ч. л'),
        ('tablespoon', 'ст. л'),
        ('glass', 'стакан'),
        ('drop', 'капля'),
        ('pinch', 'щепотка'),
        ('handful', 'горсть'),
        ('piece', 'кусок'),
        ('thing', 'шт.'),
        ('bunch', 'пучок'),
        ('segment', 'долька'),
        ('jar', 'банка'),
        ('pack', 'упаковка'),
        ('clove', 'зубчик'),
        ('carcass', 'тушка'),
        ('pod', 'стручок'),
        ('bottle', 'бутылка'),
        ('sprig', 'веточка'),
        ('loaf', 'батон'),
        ('bag', 'пакетик'),
        ('package', 'пакетик'),
        ('leaf', 'лист'),
        ('stalk', 'стебель'),
    ]
    name = CharField(
        verbose_name='Ингридиент',
        max_length=200,
        unique=True,
    )
    measurement_unit = CharField(
        verbose_name='Единицы измерения',
        max_length=200,
        #  choices=MEASURES,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name', )
        constraints = (
            CheckConstraint(
                check=Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
            CheckConstraint(
                check=Q(measurement_unit__length__gt=0),
                name='\n%(app_label)s_%(class)s_measurement_unit is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}'


class Recipe(Model):
    '''Модель для рецептов'''
    author = ForeignKey(
        verbose_name='Автор рецепта',
        to=User,
        on_delete=CASCADE
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    ingredients = ManyToManyField(
        verbose_name='Ингредиенты блюда',
        to=Ingredient,
        through='recipes.QuantityIngredient',
        related_name='recipes',
    )
    tags = ManyToManyField(
        verbose_name='Тег',
        to='Tag',
        related_name='recipes',
    )
    image = ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/'
    )
    name = CharField(
        verbose_name='Название блюда',
        max_length=200,
    )
    text = TextField(
        verbose_name='Описание блюда',
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0,
        validators=(
            MinValueValidator(
                1,
                'Ваше блюдо уже готово!'
            ),
            MaxValueValidator(
                600,
                'Очень долго ждать...'
            ),
        )
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )
        constraints = (
            UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author'
            ),
            CheckConstraint(
                check=Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author.username}'

    def number_adds(self):
        return self.favorites.all().count()

    def get_ingredients(self):
        ingredients = [i.name for i in self.ingredients.all()]
        if not ingredients:
            return 'No ingredients'
        return ingredients


class QuantityIngredient(Model):
    '''Количество ингридиентов в блюде.'''
    recipe = ForeignKey(
        to=Recipe,
        related_name='quantity',
        on_delete=CASCADE,
    )
    ingredient = ForeignKey(
        to=Ingredient,
        related_name='quantity',
        on_delete=CASCADE,
    )
    quantity = PositiveSmallIntegerField(
        default=0,
        validators=(
            MinValueValidator(
                1, 'Нужно хоть какое-то количество.'
            ),
            MaxValueValidator(
                10000, 'Слишком много!'
            ),
        )
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'ingredient', ),
                name='\n%(app_label)s_%(class)s ingredients alredy added\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.quantity} {self.ingredient} в {self.recipe}'


class Subscription(Model):
    '''Подписки на авторов.'''
    subscriber = ForeignKey(
        verbose_name='Подписчик',
        related_name='subscriber',
        to=User,
        on_delete=CASCADE
    )
    author = ForeignKey(
        verbose_name='Автор',
        related_name='following',
        to=User,
        on_delete=CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('subscriber', )
        constraints = (
            UniqueConstraint(
                fields=('subscriber', 'author'),
                name='\n%(app_label)s_%(class)s_already_exist\n',
            ),
            CheckConstraint(
                check=~Q(subscriber=F('author')),
                name='\n%(app_label)s_%(class)s_no_self_subscribe\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.subscriber} --> {self.author}'


class Favorite(Model):
    '''Избранные рецепты.
    Внимание!!!
    Django не решает проблему ограничений на уровне базы по связанным PK.
    Если вам нужно запретить "owner == recipe.author",
    Позаботьтесь об этом в контроллерах. '''
    owner = ForeignKey(
        verbose_name='Владелец подписки',
        related_name='owner',
        to=User,
        on_delete=CASCADE,
    )
    recipe = ForeignKey(
        verbose_name='Понравившиеся рецепты',
        related_name='favorites',
        to='Recipe',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Понравившейся рецепт'
        verbose_name_plural = 'Понравившиеся рецепты'
        ordering = ('recipe', 'owner', )
        constraints = (
            UniqueConstraint(
                fields=('owner', 'recipe'),
                name='\n%(app_label)s_%(class)s recipe alredy added\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.owner}: {self.recipe}'
