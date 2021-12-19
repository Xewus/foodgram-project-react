from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (IngredientSerializer, RecipePutSerializer,
                          RecipeSerializer, TagSerializer, UserSerializer)
from .servises import add_del_object

User = get_user_model()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('^name', )


class RecipeViewSet(ModelViewSet):
    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited == '1':
            user = self.request.user
            queryset = queryset.filter(favorites__owner=user)
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return RecipePutSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=('get', 'delete'), detail=True)
    def favorite(self, request, pk):
        return add_del_object(self, pk, Favorite)

    @action(methods=('get', 'delete'), detail=True)
    def shopping_cart(self, request, pk):
        return add_del_object(self, pk, ShoppingCart)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
