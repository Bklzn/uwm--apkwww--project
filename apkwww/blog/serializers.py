import datetime

from rest_framework import serializers
from .models import Post, Comment, Categories
from django.contrib.auth.models import User
from django.utils import timezone


def validate_published_date(published_date):
    if published_date < timezone.now():
        raise serializers.ValidationError('Date cannot be from past!')
    return published_date


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length = 200)
    text = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset = Categories.objects.all(), allow_null = True)
    author = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    created_date = serializers.DateTimeField(read_only=True)
    published_date = serializers.DateTimeField(validators=[validate_published_date])

    def create(self, data):
        return Post.objects.create(**data)

    def update(self, instance, data):
        instance.title = data.get('title', instance.title)
        instance.text = data.get('text', instance.text)
        instance.author = data.get('author', instance.author)
        instance.created_date = data.get('created_date', instance.created_date)
        instance.published_date = data.get('published_date', instance.published_date)
        instance.category = data.get('category', instance.category)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    author = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), allow_null = True)
    nickname = serializers.CharField(max_length=35, allow_null=True)
    created_date = serializers.DateTimeField(read_only=True)
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

        if data['author'] is None and data['nickname'] is None:
            raise serializers.ValidationError("author and nickname can't be null, at least one has to have value.")

        return data


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.CharField(max_length=40, allow_null=False)
    description = serializers.CharField(max_length=100, allow_null=True)

    def create(self, data):
        return Categories.objects.create(**data)

    def update(self, instance, data):
        instance.category = data.get('category', instance.category)
        instance.description = data.get('description', instance.description)
        instance.save()
        return instance
