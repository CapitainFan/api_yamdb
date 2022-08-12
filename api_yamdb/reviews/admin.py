from django.contrib import admin
from .models import Category, Genre, Title, Comment, Review


class Admin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'author', 'title')
    search_fields = ('title', 'author')
    list_filter = ('score', 'text',)
    empty_value_display = '-пусто-'


admin.site.register(Review, Admin)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Comment)
