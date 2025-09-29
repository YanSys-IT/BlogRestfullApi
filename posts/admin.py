
from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'content', 'image')
    list_display = ('title', 'author', 'created_at')

    def save_model(self, request, obj, form, change):
        # Only assign the request user as author if not set and the user is authenticated.
        if not obj.author_id and getattr(request.user, 'is_authenticated', False):
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at', 'author')


