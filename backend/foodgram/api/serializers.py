from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientInRecipe,
    Favorite,
    ShoppingList
)
from users.models import AuthorSubscription
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(UserSerializer):
    """
    Сериализатор для пользователя.

    Используется для:
    - Списка пользователей
    - Профиля пользователя
    - Текущего пользователя
    
    Сериализаторы для:
    - Регистрации пользователя
    - Изменения пароля
    - Получения токена
    - Удаления токена
    используются из бибилиотеки Djoser.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        """Метод проверят подписан ли пользователь на автора."""

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AuthorSubscription.objects.filter(
                subscriber=request.user,
                author=obj
            ).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для рецептов."""


#\    class Meta:
#        model = Recipe
#        fields = 


