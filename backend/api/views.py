from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F
from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import AmountIngredient, Ingredient, Recipe, Tag

from .serializers import (AddDelSerializer, IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserSerializer,
                          UserSubscribeSerializer)
from .services import (AdminOrReadOnly, AuthorStaffOrReadOnly,
                       PageLimitPagination, add_del_obj)

User = get_user_model()
SYMBOL_FOR_SEARCH = ('1', 'true',)


class UserViewSet(DjoserUserViewSet):
    '''
    ViewSet для работы с пользователми - вывод таковых,
    регистрация.
    Для авторизованных пользователей —
    возможность подписаться на автора рецепта.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination

    @action(methods=('get', 'post', 'delete',), detail=True)
    def subscribe(self, request, id,):
        '''
        Создаёт либо удалет объект связи между запрашивающим
        и запрошенным пользователями.
        Вызов метода через url: */user/<int:id>/subscribe/.
        '''
        user = self.request.user
        serializer = UserSubscribeSerializer
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return add_del_obj(
            self, id, user.subscribe, User, serializer, request
        )

    @action(methods=('get',), detail=False)
    def subscriptions(self, request):
        '''
        Выводит список пользоваетелей
        на каторых подписан запрашивающй пользователь
        Вызов метода через url: */user/<int:id>/subscribtions/.
        '''
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
    '''
    ViewSet для работы с тэгами.
    Изменение и создание объектов разрешено только админам.
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    '''
    ViewSet для работы с игридиентами.
    Изменение и создание объектов разрешено только админам.
    '''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None
    filter_backends = (SearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(ModelViewSet):
    '''
    ViewSet для работы с рецептами - вывод, создание, редактирование,
    добавление/удаление в избранное и список покупок.
    Отправка текстового файла со списком покупок.
    Для авторизованных пользователей — возможность добавить
    рецепт в избранное и в список покупок.
    Изменять рецепт может только автор или админы.
    '''
    serializer_class = RecipeSerializer
    permission_classes = (AuthorStaffOrReadOnly,)
    pagination_class = PageLimitPagination

    def get_queryset(self):
        queryset = Recipe.objects.all().select_related('author')
        user = self.request.user

        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        is_in_shopping = self.request.query_params.get('is_in_shopping_cart')
        if is_in_shopping in SYMBOL_FOR_SEARCH:
            if not user.is_anonymous:
                queryset = queryset.filter(cart=user.id)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in SYMBOL_FOR_SEARCH:
            if not user.is_anonymous:
                queryset = queryset.filter(favorite=user.id)

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        return queryset

    @action(methods=('get', 'delete', 'post'), detail=True)
    def favorite(self, request, pk):
        '''
        Добавляет либо удалет рецепт в "избранное".
        Вызов метода через url:  */recipe/<int:id>/favorite/.
        '''
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return add_del_obj(self, pk, user.favorites, Recipe, AddDelSerializer)

    @action(methods=('get', 'delete', 'post'), detail=True)
    def shopping_cart(self, request, pk):
        '''
        Добавляет либо удалет рецепт в "список покупок".
        Вызов метода через url:  */recipe/<int:id>/shopping_cart/.
        '''
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return add_del_obj(self, pk, user.carts, Recipe, AddDelSerializer)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        '''
        Считает сумму ингредиентов в рецептах выбранных для покупки.
        Возвращает текстовый файл со списком ингредиентов.
        Вызов метода через url:  */recipe/<int:id>/download_shopping_cart/.
        '''
        user = self.request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        recipes = user.carts.values('id')
        ingredients = AmountIngredient.objects.filter(
            recipe__in=recipes
        ).values(
            'amount',
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        )

        shopping_list = {}
        for i in ingredients:
            if i['ingredient'] not in shopping_list:
                shopping_list[i['ingredient']] = [i['amount'], i['measure']]
            else:
                shopping_list[i['ingredient']][0] += i['amount']

        filename = f'{user}_shopping_list.txt'
        filepath = settings.MEDIA_ROOT / filename
        with open(filepath, 'w') as file:
            file.write(
                f'Список покупок\n\n{user}\n\n{dt.now()}\n\n'
            )
            for key, value in shopping_list.items():
                file.write(f'{key}: {value[0]} {value[1]} \n')

        shopping_list = open(filepath, 'r')
        response = HttpResponse(shopping_list, content_type='text.txt')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
