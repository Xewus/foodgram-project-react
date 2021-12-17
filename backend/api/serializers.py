from rest_framework.serializers import ModelSerializer

from ..recipes.models import Favorite, Ingredient, Subscription, Tag
from ..users import MyUser as User


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class FavoriteSerializer(ModelSerializer):

    class Meta:
        model = Favorite

        fields = '__all__'


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password',
        )
