from django.db import models
from django.utils import timezone
from django.contrib import auth

class Post(models.Model):
    title = models.CharField(max_length = 200)
    text = models.TextField()
    author = models.ForeignKey('auth.User', null = True, on_delete = models.CASCADE)
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey('auth.User', null = True, blank = True, on_delete = models.CASCADE)
    created_date = models.DateTimeField(default = timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def text_cut(self):
        if len(self.text) > 15:
            return f'{self.text[:15]}.....'
        return self.text
        
    text_cut.short_description = "Comment"
