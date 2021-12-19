from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet, 'recipes')
router.register('users', UserViewSet)

urlpatterns = (
    path('auth/', include('users.urls', namespace='users')),
    path('', include(router.urls)),
)
