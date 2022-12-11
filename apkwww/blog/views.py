from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment, Categories
from django.db.models import Q
from .serializers import PostSerializer, CommentSerializer, CategorySerializer
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
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        post = Post(**request.data)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        return Response([serializerPost.data, serializerComments.data], status=status.HTTP_200_OK)
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
    if len(contains) < 3:
        return Response({"Error": "Type 3 or more characters"}, status=status.HTTP_403_FORBIDDEN)
    elif post.count() == 0:
        return Response({"Error": "No matching posts"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializerPost = PostSerializer(post, many = True)
        return Response([serializerPost.data], status=status.HTTP_200_OK)

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
        return Response([serializerPost.data, serializerComments.data], status=status.HTTP_200_OK)

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
    return Response([{"profile": user.__str__(), "number of posts": posts_num,"number of comments": comments_num},serializerPost.data, serializerComments.data], status=status.HTTP_200_OK)

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
        return Response([{"profile": user.__str__(), "number of posts": posts_num,"number of comments": comments_num},serializerPost.data, serializerComments.data], status=status.HTTP_200_OK)

@api_view(['GET','DELETE'])
def comments_view_by_id(request, pk):
    try:
        comment = Comment.objects.get(pk = pk)
    except comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializerComment = CommentSerializer(comment)
        return Response(serializerComment.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','DELETE'])
def comment_of_the_post(request, postID, comID):
    try:
        post = Post.objects.get(pk = postID)
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        comments = Comment.objects.filter(post = post).order_by("-created_date")
        if comID > len(comments):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializerCom = CommentSerializer(comments[comID - 1])
        return Response(serializerCom.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def comments_of_the_post_by_str(request, postID, contains):
    try:
        post = Post.objects.get(pk = postID)
    except post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        comments = Comment.objects.filter(
            Q(text__icontains = contains) &
            Q(post = post)).order_by('-created_date')
        if len(contains) < 3:
            return Response({"Error": "Type 3 or more characters"}, status=status.HTTP_403_FORBIDDEN)
        elif comments.count() == 0:
            return Response({"Error": "No matching posts"}, status=status.HTTP_404_NOT_FOUND)
        serializerCom = CommentSerializer(comments, many = True)
        return Response(serializerCom.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_view(request):
    categories = Categories.objects.all()
    serializerCat = CategorySerializer(categories, many = True)
    return Response(serializerCat.data, status = status.HTTP_200_OK)

@api_view(['GET'])
def category_byId(request, id):
    try:
        category = Categories.objects.get(pk = id)
    except category.DoesNotExist:
        return Response({"Error": "No matching category"}, status=status.HTTP_404_NOT_FOUND)
    posts = Post.objects.filter(category = category)
    serializerPost = PostSerializer(posts, many = True)
    serializerCat = CategorySerializer(category)
    return Response([serializerCat.data, serializerPost.data], status = status.HTTP_200_OK)

@api_view(['GET'])
def category_byName(request, cat):
    try:
        category = Categories.objects.get(category = cat)
    except:
        return Response({"Error": "No matching category"}, status=status.HTTP_404_NOT_FOUND)
    posts = Post.objects.filter(category = category)
    serializerPost = PostSerializer(posts, many = True)
    serializerCat = CategorySerializer(category)
    return Response([serializerCat.data, serializerPost.data], status = status.HTTP_200_OK)
