from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUser_Admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Category, Comment, Location, Post

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUser_Admin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'posts_count'
    )

    @admin.display(description='Кол-во постов у пользователя')
    def posts_count(self, obj):
        return obj.posts.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'description',
        'slug'
    )
    list_editable = ('is_published',)
    search_fields = ('title',)
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'pub_date',
        'location',
        'category'
    )
    list_editable = (
        'is_published',
        'location',
        'category'
    )
    search_fields = ('title', 'text')
    list_filter = ('is_published', 'location', 'category')
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'created_at',
        'post'
    )
    list_filter = ('author', 'created_at')
