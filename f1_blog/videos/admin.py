from django.contrib import admin
from f1_blog.videos.models import Video, Comment


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'video', 'author', 'get_likes_count', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['video', 'author', 'text', 'get_likes_count', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()
