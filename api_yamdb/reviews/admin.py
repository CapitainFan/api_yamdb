from django.contrib import admin
from .models import Title, Comment, Review


class Admin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'author', 'title')
    search_fields = ('title', 'author')
    list_filter = ('score', 'text',)
    empty_value_display = '-пусто-'


admin.site.register(Title)
admin.site.register(Review, Admin)
admin.site.register(Comment)
