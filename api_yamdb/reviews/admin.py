from django.conf import settings
from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role',)
    search_fields = ('email',)


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date',)
    search_fields = ('text',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Review)
class CommentAdminReview(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'score', 'pub_date',)
    search_fields = ('text',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'year', 'category',)
    search_fields = ('name',)
    list_filter = ('name',)
