from django.shortcuts import get_object_or_404
from recipes.models import AmountIngredient, Recipe
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (BasePermission,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)


class AuthorStaffOrReadOnly(IsAuthenticatedOrReadOnly):
    '''
    Разрешение на создание и изменение только для админов и автора.
    Остальным только чтение объекта.
    '''
    def has_object_permission(self, request, view, obj):
        return (
            request.method in ('GET',)
            or (request.user == obj.author)
            or request.user.is_moderator
            or request.user.is_admin
        )


class AdminOrReadOnly(BasePermission):
    '''
    Разрешение на создание и изменение только для админов.
    Остальным только чтение объекта.
    '''
    def has_permission(self, request, view):
        return (
            request.method in ('GET',)
            or request.user.is_authenticated
            and request.user.is_admin
        )


class PageLimitPagination(PageNumberPagination):
    '''
    Стандартный пагинатор.
    Переименовано имя параметра под требования фронтенда.
    '''
    page_size_query_param = 'limit'


def set_amount_ingredients(recipe, ingredients):
    '''
    Записывает ингредиенты вложенные в рецепт.
    '''
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ing'],
            amount=ingredient['amount']
        )


def add_del_recipe(self, pk, klass, serializer):
    '''
    This method adds objects "many-to-many"
    relationed "User" and "Recipe".
    Should use it with http.methods "GET", "POST", "DELETE".
    The related object necessarily has fields in position:
    Klass(user, recipe).
    '''
    user = self.request.user
    if user.is_anonymous:
        return Response(status=HTTP_401_UNAUTHORIZED)
    recipe = get_object_or_404(Recipe, id=pk)

    serializer = serializer(recipe)

    if self.request.method in ('GET', 'POST',):
        obj, created = klass.objects.get_or_create(owner=user, recipes=recipe)

        if created:
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)

    if self.request.method in ('DELETE',):
        obj = get_object_or_404(klass, owner=user, recipes=recipe)
        obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    return Response(status=HTTP_400_BAD_REQUEST)
