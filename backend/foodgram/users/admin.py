from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, AuthorSubscription

class Admin(admin.ModelAdmin):
    list_filter = (
        'username',
        'email'
    )

    list_display = (
        'email',
        'username'
    )
# Не добавляем поля через UserAdmin.fieldsets,
# а сразу регистрируем модель в админке:
admin.site.register(User, Admin)
admin.site.register(AuthorSubscription)