from atexit import register
from django.contrib import admin

from .models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'
