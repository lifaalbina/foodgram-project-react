from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Tag(models.Model):
    """
    Модель для хранения информации о тегах.

    Поля модели:
    - name: Название тега.
    - color_code: Цветовой код тега.
    - slug: Человеко-читаемый идентификатор для URL (уникальный).
    """

    name = models.CharField(
        'Название',
        max_length=settings.MAX_LENGTH_RECIPE_PARAMS,
    )
    color_code = models.CharField(
        'Цвет',
        max_length=7,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=settings.MAX_LENGTH_RECIPE_PARAMS,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для хранения информации об ингредиентах.

    Поля модели:
    - name: Название ингредиента.
    - measurement_unit: Единица измерения ингредиента.
    """

    GRAM = 'гр'
    MILLILITER = 'мл'
    PIECE = 'шт'
    KILOGRAM = 'кг'
    LITER = 'л'
    TEASPOON = 'ч. л.'
    TABLESPOON = 'ст. л.'

    MEASUREMENT_UNIT_CHOICES = [
        (GRAM, 'гр'),
        (MILLILITER, 'мл'),
        (PIECE, 'шт'),
        (KILOGRAM, 'кг'),
        (LITER, 'л'),
        (TEASPOON, 'ч. л.'),
        (TABLESPOON, 'ст. л.')
    ]

    name = models.CharField(
        'Название',
        max_length=settings.MAX_LENGTH_RECIPE_PARAMS
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=50,
        choices=MEASUREMENT_UNIT_CHOICES,
        blank=False
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель для хранения информации о рецептах.

    Поля модели:
    - author: Автор публикации (пользователь).
    - name: Название рецепта.
    - image: Картинка рецепта.
    - description: Текстовое описание рецепта.
    - ingredients: Ингредиенты для приготовления блюда (множественное поле).
    - tags: Теги, установленные для рецепта (множественное поле).
    - cooking_time: Время приготовления в минутах.
    - created_at: Дата и время создания рецепта.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название',
        max_length=settings.MAX_LENGTH_RECIPE_PARAMS
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipe_images/',
        blank=True,
        null=True
    )  # потом убрать бланк и нул
    text = models.TextField('Текстовое описание')
    ingredients = models.ManyToManyField(
        'Ingredient', through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField('Время приготовления в минутах')
    created_at = models.DateTimeField(
        'Дата и время создания',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """
    Модель для отношения между рецептом и ингредиентом.

    Поля модели:
    - ingredient: Внешний ключ к модели Ingredient.
    - recipe: Внешний ключ к модели Recipe.
    - quantity: Количество ингредиента в рецепте.
    """

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    quantity = models.FloatField('Количество')

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self) -> str:
        return f'{self.ingredient} в {self.recipe}'


class Favorite(models.Model):
    """Модель для избранного.

    Поля модели:
    - user: Внешний ключ к модели User
    - recipe: Внешний ключ к модели Recipe
    """

    user = models.ForeignKey(
        User,
        verbose_name='User',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='User favorite recipe',
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_favorites',
            ),
        )


class ShoppingList(models.Model):
    """Модель для списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        
    def __str__(self) -> str:
        return f'{self.user} - {self.recipe}'
