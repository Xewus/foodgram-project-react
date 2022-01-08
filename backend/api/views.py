from datetime import datetime as dt
from urllib.parse import unquote

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http.response import HttpResponse

from djoser.views import UserViewSet as DjoserUserViewSet

from recipes.models import AmountIngredient, Ingredient, Recipe, Tag

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import tuns as t
from .paginators import PageLimitPagination
from .permissions import AdminOrReadOnly, AuthorStaffOrReadOnly
from .serializers import (AddDelSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer,
                          UserSubscribeSerializer)
from .services import add_del_obj

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    """
    ViewSet для работы с пользователми - вывод таковых,
    регистрация.
    Для авторизованных пользователей —
    возможность подписаться на автора рецепта.
    """
    queryset = User.objects.all()
    pagination_class = PageLimitPagination

    @action(methods=t.ACTION_METHODS, detail=True)
    def subscribe(self, request, id,):
        """
        Создаёт либо удалет объект связи между запрашивающим
        и запрошенным пользователями.
        Вызов метода через url: */user/<int:id>/subscribe/.
        """
        user = self.request.user
        serializer = UserSubscribeSerializer
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return add_del_obj(
            self, id, user.subscribe, User, serializer, request
        )

    @action(methods=('get',), detail=False)
    def subscriptions(self, request):
        """
        Выводит список пользоваетелей
        на каторых подписан запрашивающй пользователь
        Вызов метода через url: */user/<int:id>/subscribtions/.
        """
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = user.subscribe.all()
        pages = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с тэгами.
    Изменение и создание объектов разрешено только админам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с игридиентами.
    Изменение и создание объектов разрешено только админам.
    """
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get(t.SEARCH_ING_NAME)
        if name:
            name = unquote(name)
            stw_queryset = list(queryset.filter(name__startswith=name))
            cnt_queryset = queryset.filter(name__contains=name)
            stw_queryset.extend(
                [i for i in cnt_queryset if i not in stw_queryset]
            )
            queryset = stw_queryset
        return queryset


class RecipeViewSet(ModelViewSet):
    """
    ViewSet для работы с рецептами - вывод, создание, редактирование,
    добавление/удаление в избранное и список покупок.
    Отправка текстового файла со списком покупок.
    Для авторизованных пользователей — возможность добавить
    рецепт в избранное и в список покупок.
    Изменять рецепт может только автор или админы.
    """
    serializer_class = RecipeSerializer
    permission_classes = (AuthorStaffOrReadOnly,)
    pagination_class = PageLimitPagination

    def get_queryset(self):
        queryset = Recipe.objects.all().select_related(t.AUTHOR)
        user = self.request.user

        tags = self.request.query_params.getlist(t.TAGS)
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get(t.AUTHOR)
        if author:
            queryset = queryset.filter(author=author)

        # Следующие фильтры только для авторизованного пользователя
        if user.is_anonymous:
            return queryset

        is_in_shopping = self.request.query_params.get(t.SHOP_CART)
        if is_in_shopping in t.SYMBOL_TRUE_SEARCH:
            queryset = queryset.filter(cart=user.id)
        elif is_in_shopping in t.SYMBOL_FALSE_SEARCH:
            queryset = queryset.exclude(cart=user.id)

        is_favorited = self.request.query_params.get(t.FAVORITE)
        if is_favorited in t.SYMBOL_TRUE_SEARCH:
            queryset = queryset.filter(favorite=user.id)
        if is_favorited in t.SYMBOL_FALSE_SEARCH:
            queryset = queryset.exclude(favorite=user.id)

        return queryset

    @action(methods=t.ACTION_METHODS, detail=True)
    def favorite(self, request, pk):
        """
        Добавляет либо удалет рецепт в "избранное".
        Вызов метода через url:  */recipe/<int:id>/favorite/.
        """
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return add_del_obj(self, pk, user.favorites, Recipe, AddDelSerializer)

    @action(methods=t.ACTION_METHODS, detail=True)
    def shopping_cart(self, request, pk):
        """
        Добавляет либо удалет рецепт в "список покупок".
        Вызов метода через url:  */recipe/<int:id>/shopping_cart/.
        """
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return add_del_obj(self, pk, user.carts, Recipe, AddDelSerializer)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        """
        Считает сумму ингредиентов в рецептах выбранных для покупки.
        Возвращает текстовый файл со списком ингредиентов.
        Вызов метода через url:  */recipe/<int:id>/download_shopping_cart/.
        """
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = AmountIngredient.objects.filter(
            recipe__in=(user.carts.values('id'))
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))

        filename = f'{user}_shopping_list.txt'
        filepath = settings.MEDIA_ROOT / filename
        with open(filepath, 'w') as file:
            file.write(
                f'Список покупок\n\n{user}\n\n{dt.now()}\n\n'
            )
            for ing in ingredients:
                file.write(
                    f"{ing['ingredient']}: {ing['amount']} {ing['measure']}\n"
                )
            file.write(
                '\nПосчитано в Foodgram.ml\n'
            )

        shopping_list = open(filepath, 'r')
        response = HttpResponse(shopping_list, content_type='text.txt')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
