from django.contrib import admin

from .models import Comment, Follow, Group, Post


class GroupAdmin(admin.ModelAdmin):
    """Поля модели Group доступные в admin"""
    list_display = ('pk', 'title', 'slug', 'description',)


class PostAdmin(admin.ModelAdmin):
    """Поля модели Post доступные в admin"""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group',)
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """Поля модели Comment доступные в admin"""
    list_display = ('pk', 'post', 'author', 'text', 'created',)


class FollowAdmin(admin.ModelAdmin):
    """Поля модели Comment доступные в admin"""
    list_display = ('pk', 'user', 'author',)


admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
