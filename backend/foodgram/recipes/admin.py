from django.contrib import admin
from .models import (
    Tag,
    Ingredient,
    Recipe,
    IngredientInRecipe,
    Favorite,
    ShoppingList
    )


class IngredientInRecipeAdmin(admin.TabularInline):
    """Настройка отображения ингредиентов в разделе Рецепты."""

    model = IngredientInRecipe
    extra = 5


class RecipeAdmin(admin.ModelAdmin):
    """Настройка админ зоны Рецептов."""

    list_display = (
        'id',
        'name',
        'author',
        'counting_favorites'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    filter_horizontal = ('tags',)
    inlines = (IngredientInRecipeAdmin,)

    def counting_favorites(self, obj):
        """Подсчет добавлений в избранное."""
        return Favorite.objects.filter(recipe=obj).count()
    counting_favorites.short_description = 'Количество добавлений в избранное'


class IngredientAdmin(admin.ModelAdmin):
    """Настройка админ зоны Ингредиентов."""

    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientInRecipe)
admin.site.register(ShoppingList)
