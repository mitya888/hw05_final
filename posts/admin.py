from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    """Класс PostAdmin используется для создания интерфейса в админпанели
    со свойствами:

    Properties
    ----------
    list_display :
        перечисляем поля, которые должны отображаться в админке
    search_fields :
        добавляем интерфейс для поиска по тексту постов
    list_filter :
        добавляем возможность фильтрации по дате
    empty_value_display :
        это свойство сработает для всех колонок: где пусто -
        там будет эта строка"""

    list_display = ("pk", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    """Класс ModelAdmin используется для создания интерфейса в админпанели
    со свойствами:

    Properties
    ----------
    title :
        перечисляем поля, которые должны отображаться в админке"""

    title = ("pk", "title", "slug", "description")
    search_fields = ("pk", "title", "slug", "description",)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ("post", "author", "text", "created")


# @admin.register(models.Follow)
# class FollowAdmin(admin.ModelAdmin):
#     list_display = ("user", "author")
#     search_fields = ("user",)
#     list_filter = ("user",)
#     empty_value_display = "-пусто-"