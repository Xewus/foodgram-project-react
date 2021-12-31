from django.contrib.auth import get_user_model
from django.db.models import F, Q
from datetime import datetime as dt
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Subscription, Tag)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (IngredientSerializer,
                          RecipeSerializer, TagSerializer,
                          UserSubscribeSerializer, UserSerializer)
from .services import PageLimitPagination, add_del_recipe

User = get_user_model()
SYMBOL_FOR_SEARCH = ('1', 'true',)


class UserViewSet(DjoserUserViewSet):
    '''
    ViewSet для работы с пользователми - вывод таковых,
    регистрация, подписки.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination

    @action(methods=('get', 'post', 'delete',), detail=True)
    def subscribe(self, request, id,):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        author = get_object_or_404(User, id=id)
        serializer = UserSubscribeSerializer(
            author, context={'request': request}
        )

        if self.request.method in ('GET', 'POST',):
            obj, created = Subscription.objects.get_or_create(
                owner=user, author=author
            )
            if created:
                return Response(serializer.data, status=HTTP_201_CREATED)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
        if self.request.method in ('DELETE',):
            obj = get_object_or_404(Subscription, owner=user, author=author)
            obj.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = User.objects.filter(following__owner=user)
        pages = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    '''
    ViewSet для работы с тэгами.
    '''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    '''
    ViewSet для работы с игридиентами.
    '''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(ModelViewSet):
    '''
    ViewSet для работы с рецептами - вывод, создание, редактирование,
    добавление/удаление в избранное и список покупок.
    '''
    serializer_class = RecipeSerializer
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
                queryset = queryset.filter(shopping_cart__owner=user)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in SYMBOL_FOR_SEARCH:
            if not user.is_anonymous:
                queryset = queryset.filter(favorites__owner=user)

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        return queryset

    @action(methods=('get', 'delete', 'post'), detail=True)
    def favorite(self, request, pk):
        return add_del_recipe(self, pk, Favorite)

    @action(methods=('get', 'delete', 'post'), detail=True)
    def shopping_cart(self, request, pk):
        return add_del_recipe(self, pk, ShoppingCart)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        '''
        Считает сумму ингредиентов в рецептах выбранных для покупки.
        Возвращает текстовый файл со списком ингредиентов.
        '''
        user = self.request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        recipes = Recipe.objects.filter(
            shopping_cart__owner=user
        ).values('id')
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
