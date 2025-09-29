
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Регистрируем нашу кастомную модель пользователя
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Поля, которые будут отображаться в админке
    list_display = ('username', 'email', 'birth_date', 'is_staff')
    # Поля, по которым можно фильтровать
    list_filter = ('is_staff', 'is_superuser', 'is_active')
