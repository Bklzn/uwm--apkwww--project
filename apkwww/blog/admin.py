from django.contrib import admin
from .models import Post, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text_cut','author', 'created_date')
    list_filter = ('author', 'created_date')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date')
    list_filter = ('author', 'created_date', 'published_date')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
