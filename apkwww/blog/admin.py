from django.contrib import admin
from .models import Post, Comment, Categories

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text_cut','post', 'author', 'created_date')
    list_filter = ('author', 'created_date')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'author', 'created_date', 'published_date')
    list_filter = ('category', 'author', 'created_date', 'published_date')

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('category','description')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Categories, CategoriesAdmin)
