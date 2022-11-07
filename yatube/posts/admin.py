"""Связь приложения Posts с админ панелью сайта"""
from django.contrib import admin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    """Регистрация модели Post в админке и её настройка
    """
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group',)
    empty_value_display = '-пусто-'


"""Регистрация моделей админке
"""
admin.site.register(Post, PostAdmin)
admin.site.register(Group)
