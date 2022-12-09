from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment
from django.db.models import Q
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET','PUT'])
def index(request):
    if request.method == 'GET':
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        post = Post(**request.data)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def posts_all(request):
    if request.method == 'GET':
        post = Post.objects.all()
        serializerPost = PostSerializer(post, many = True)
        return Response(serializerPost.data)
@api_view(['GET','PUT', 'DELETE'])
def post_view(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
        for com in comments:
            com.text = com.text_cut()
        serializerPost = PostSerializer(post)
        serializerComments = CommentSerializer(comments, many = True)
        return Response([serializerPost.data, serializerComments.data])
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def post_search(request, contains):
    post = Post.objects.filter(
        Q(text__icontains = contains) |
        Q(title__icontains = contains) &
        Q(published_date__isnull = False)).order_by('-published_date')
    if post.count() == 0:
        return Response({"Error": "No matching posts"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializerPost = PostSerializer(post, many = True)
        return Response([serializerPost.data])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
    try:
        posts = Post.objects.filter(author = request.user)
    except len(posts) == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        posts = Post.objects.filter(author = request.user).order_by('-created_date')
        comments = Comment.objects.filter(author=request.user).order_by("-created_date")
        for com in comments:
            com.text = com.text_cut()
        serializerPost = PostSerializer(posts, many = True)
        serializerComments = CommentSerializer(comments, many = True)
        return Response([serializerPost.data, serializerComments.data])

@api_view(['GET'])
def profile_view_by_id(request, pk):
    user = User.objects.get(id = pk)
    posts = Post.objects.filter(author = user).order_by('-published_date')
    posts_num = posts.count()
    comments = Comment.objects.filter(author = user).order_by("-created_date")
    comments_num = comments.count()
    for com in comments:
        com.text = com.text_cut()
    serializerPost = PostSerializer(posts, many = True)
    serializerComments = CommentSerializer(comments, many = True)
    print(serializerComments.data)
    return Response([{"profile": user.__str__(), "number of posts": posts_num,"number of comments": comments_num},serializerPost.data, serializerComments.data])

@api_view(['GET'])
def profile_view_by_string(request, name):
    try:
        user = User.objects.get(username = name)
    except:
        return Response({"Error": "User with that name does not exist"},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        posts = Post.objects.filter(author = user).order_by('-published_date')
        posts_num = posts.count()
        comments = Comment.objects.filter(author = user).order_by("-created_date")
        comments_num = comments.count()
        for com in comments:
            com.text = com.text_cut()
        serializerPost = PostSerializer(posts, many = True)
        serializerComments = CommentSerializer(comments, many = True)
        print(serializerComments.data)
        return Response([{"profile": user.__str__(), "number of posts": posts_num,"number of comments": comments_num},serializerPost.data, serializerComments.data])