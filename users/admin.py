
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'birth_date', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
