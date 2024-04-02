from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный пользователь."""

    email = models.EmailField(
        'Почта',
        max_length=settings.MAX_EMAIL_LENGTH
    )
    username = models.CharField(
        'Логин',
        max_length=settings.MAX_LENGTH_FOR_USER_PARAMS,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.MAX_LENGTH_FOR_USER_PARAMS
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.MAX_LENGTH_FOR_USER_PARAMS
    )
    password = models.CharField(
        'Пароль',
        max_length=settings.MAX_LENGTH_FOR_USER_PARAMS
    )

    class Meta:
        """Дополнительные настройки админ панели."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class AuthorSubscription(models.Model):
    """Модель подписки на автора рецепта.

    Поля модели:
    - subscriber: Поле для связи с пользователем, который подписывается.
    - author: Поле для связи с автором, на которого подписываются.
    """

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'author',), name="unique_subscription"
            ),
        )

    def __str__(self) -> str:
        return f'{self.subscriber} подписан на {self.author}'
