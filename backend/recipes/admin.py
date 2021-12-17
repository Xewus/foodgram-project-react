from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register, site
from django.utils.safestring import mark_safe

from .models import (Favorite, Ingredient, QuantityIngredient, Recipe,
                     Subscription, Tag)

site.site_header = 'Администрирование Foodgram'


class QuantityIngredientInline(TabularInline):
    model = QuantityIngredient
    extra = 2


@register(Favorite, QuantityIngredient, Subscription)
class LinksAdmin(ModelAdmin):
    pass


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        'name', 'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )

    save_on_top = True
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'name', 'author', 'get_ingredients', 'get_image'
        )
    fields = (
        ('name', 'cooking_time', ),
        ('author', 'tags', ),
        ('text', ),
        ('image', ),
    )
    raw_id_fields = ('author', 'tags', )
    search_fields = (
        'name', 'author',
    )
    list_filter = (
        'name', 'author__username', 'tags',
    )

    inlines = (QuantityIngredientInline,)
    save_on_top = True
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    def get_ings(self, obj):
        return Ingredient.objects.filter(recipes=obj).count()

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = 'Изображение'
    Recipe.number_adds.short_description = 'Количество добавлений'
    Recipe.get_ingredients.short_description = 'Инргедиенты'


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'name', 'color', 'slug',
    )
    search_fields = (
        'name', 'color'
    )

    save_on_top = True
    empty_value_display = settings.EMPTY_VALUE_DISPLAY
