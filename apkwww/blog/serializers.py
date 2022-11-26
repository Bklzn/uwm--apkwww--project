from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 200)
    text = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    created_date = serializers.DateTimeField()
    published_date = serializers.DateTimeField(allow_null = True)

    def create(self, data):
        return Post.objects.create(**data)

    def update(self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.text = data.get('text', instance.text)
        instance.author = data.get('author', instance.author)
        instance.created_date = data.get('created_date', instance.created_date)
        instance.published_date = data.get('published_date', instance.published_date)
        instance.save()
        return instance

class CommentSerializer(serializers.Serializer):
    text = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), allow_null = True)
    created_date = serializers.DateTimeField()
    post = serializers.PrimaryKeyRelatedField(queryset = Post.objects.all(), allow_null = False)

    def create(self, data):
        return Comment.objects.create(**data)

    def update(self, instance, data):
        instance.text = data.get('text', instance.text)
        instance.author = data.get('author', instance.author)
        instance.created_date = data.get('created_date', instance.created_date)
        instance.post = data.get('post', instance.post)
        instance.save()
        return instance

    def validate(self, data):
        if data['post'].published_date is None:
            raise serializers.ValidationError("Post must be published")
        return data