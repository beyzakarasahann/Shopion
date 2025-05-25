from django.contrib import admin
from .models import Category, Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'category')
    search_fields = ('title', 'content')
    list_editable = ('is_approved',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    list_editable = ('is_approved',)
