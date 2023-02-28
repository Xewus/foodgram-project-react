from api.views import (BaseAPIRootView, IngredientViewSet, RecipeViewSet,
                       TagViewSet, UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'


class RuDefaultRouter(DefaultRouter):
    """Показывает описание главной страницы API на русском языке.
    """
    APIRootView = BaseAPIRootView


router = RuDefaultRouter()
router.register('tags', TagViewSet, 'tags')
router.register('ingredients', IngredientViewSet, 'ingredients')
router.register('recipes', RecipeViewSet, 'recipes')
router.register('users', UserViewSet, 'users')

urlpatterns = (
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
)
