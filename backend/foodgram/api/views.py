from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from recipes.models import Tag, Ingredient, IngredientInRecipe, Recipe, Favorite, ShoppingList
from users.models import AuthorSubscription
from django.contrib.auth import get_user_model
from .serializers import TagSerializer, IngredientSerializer
User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с моделью Tag.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """
    Вюсюсет для работы с моделью Ingredient.

    Поиск по названию ингридиента не зависимо от регистра.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None

