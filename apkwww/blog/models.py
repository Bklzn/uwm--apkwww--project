from django.db import models
from django.utils import timezone
from django.contrib import auth

class Categories(models.Model):
    category = models.CharField(max_length = 40, null = False)
    description = models.TextField(max_length = 100, null = True)

    def __str__(self):
        return self.category

class Post(models.Model):
    title = models.CharField(max_length = 200)
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    category = models.ForeignKey(Categories, blank = True, null = True, on_delete = models.SET_NULL)
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True, default=timezone.now)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('auth.User', null = True, blank = True, on_delete = models.SET_NULL)
    nickname = models.CharField(max_length=35, blank = True, null = True)
    created_date = models.DateTimeField(default = timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def text_cut(self):
        if len(self.text) > 15:
            return f'{self.text[:15]}.....'
        return self.text
        
    text_cut.short_description = "Comment"
