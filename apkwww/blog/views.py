from django.utils import timezone
from .models import Post, Comment, Categories
from django.db.models import Q
from .serializers import PostSerializer, CommentSerializer, CategorySerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'PUT'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def index(request):
    if request.method == 'GET':
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            category = Categories.objects.get(id=request.data['category'])
            request.data['category'] = category
            request.data['author'] = request.user
            post = Post(**request.data)
            request.data['author'] = request.user.id
            request.data['category'] = category.id
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Zaloguj się"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def post_view(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
        for com in comments:
            com.text = com.text_cut()
        serializer_post = PostSerializer(post)
        serializer_comments = CommentSerializer(comments, many=True)
        return Response([serializer_post.data, serializer_comments.data], status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        request.data["post"] = post
        comment = Comment(**request.data)
        request.data["post"] = post.pk
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if request.user.is_authenticated and post.author == request.user:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Nie masz uprawnień, zaloguj się lub skontaktuj z autorem posta"},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def post_edit(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_post = PostSerializer(post)
        return Response(serializer_post.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if request.user == post.author and request.user.is_authenticated:
            if post.published_date is not None and ' [Edited]' not in post.title:
                post.title += ' [Edited]'
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Nie masz uprawnień, zaloguj się lub skontaktuj z autorem posta"},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def post_search(request, contains):
    post = Post.objects.filter(
        Q(text__icontains=contains) |
        Q(title__icontains=contains) &
        Q(published_date__isnull=False)).order_by('-published_date')
    if len(contains) < 3:
        return Response({"Error": "Type 3 or more characters"}, status=status.HTTP_400_BAD_REQUEST)
    elif post.count() == 0:
        return Response({"Error": "No matching posts"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_post = PostSerializer(post, many=True)
        return Response([serializer_post.data], status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def my_profile_view(request):
    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        posts = Post.objects.filter(author=request.user).order_by('-created_date')
        comments = Comment.objects.filter(author=request.user).order_by("-created_date")
        for com in comments:
            com.text = com.text_cut()
        serializer_post = PostSerializer(posts, many=True)
        serializer_comments = CommentSerializer(comments, many=True)
        return Response([serializer_post.data, serializer_comments.data], status=status.HTTP_200_OK)


@api_view(['GET'])
def profile_view_by_id(request, pk):
    user = User.objects.get(id=pk)
    posts = Post.objects.filter(author=user).order_by('-published_date')
    posts_num = posts.count()
    comments = Comment.objects.filter(author=user).order_by("-created_date")
    comments_num = comments.count()
    for com in comments:
        com.text = com.text_cut()
    serializer_post = PostSerializer(posts, many=True)
    serializer_comments = CommentSerializer(comments, many=True)
    return Response([{"profile": user.__str__(), "number of posts": posts_num, "number of comments": comments_num},
                     serializer_post.data, serializer_comments.data], status=status.HTTP_200_OK)


@api_view(['GET'])
def profile_view_by_string(request, name):
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist:
        return Response({"Error": "User with that name does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        posts = Post.objects.filter(author=user).order_by('-published_date')
        posts_num = posts.count()
        comments = Comment.objects.filter(author=user).order_by("-created_date")
        comments_num = comments.count()
        for com in comments:
            com.text = com.text_cut()
        serializer_post = PostSerializer(posts, many=True)
        serializer_comments = CommentSerializer(comments, many=True)
        return Response([{"profile": user.__str__(), "number of posts": posts_num, "number of comments": comments_num},
                         serializer_post.data, serializer_comments.data], status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def comments_view_by_id(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer_comment = CommentSerializer(comment)
        return Response(serializer_comment.data, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        if request.user.is_authenticated and request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Nie masz uprawnień, zaloguj się lub skontaktuj z autorem komentarza, lub posta"},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
def comment_of_the_post(request, post_id, com_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        comments = Comment.objects.filter(post=post).order_by("-created_date")
        if com_id > len(comments):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer_com = CommentSerializer(comments[com_id - 1])
        return Response(serializer_com.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        if request.user.is_authenticated:
            comments = Comment.objects.filter(post=post).order_by("-created_date")
            if com_id > len(comments):
                return Response(status=status.HTTP_404_NOT_FOUND)
            if request.user == post.author or request.user == comments[com_id - 1].author:
                comments[com_id - 1].delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Error": "Nie masz uprawnień, zaloguj się lub skontaktuj z autorem komentarza, lub posta"},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def comments_of_the_post_by_str(request, post_id, contains):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        comments = Comment.objects.filter(
            Q(text__icontains=contains) &
            Q(post=post)).order_by('-created_date')
        if len(contains) < 3:
            return Response({"Error": "Type 3 or more characters"}, status=status.HTTP_403_FORBIDDEN)
        elif comments.count() == 0:
            return Response({"Error": "No matching posts"}, status=status.HTTP_404_NOT_FOUND)
        serializer_com = CommentSerializer(comments, many=True)
        return Response(serializer_com.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_view(request):
    categories = Categories.objects.all()
    serializer_cat = CategorySerializer(categories, many=True)
    return Response(serializer_cat.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_by_id(request, pk):
    try:
        category = Categories.objects.get(pk=pk)
    except Categories.DoesNotExist:
        return Response({"Error": "No matching category"}, status=status.HTTP_404_NOT_FOUND)
    posts = Post.objects.filter(category=category)
    serializer_post = PostSerializer(posts, many=True)
    serializer_cat = CategorySerializer(category)
    return Response([serializer_cat.data, serializer_post.data], status=status.HTTP_200_OK)


@api_view(['GET'])
def category_by_name(request, cat):
    try:
        category = Categories.objects.get(category=cat)
    except Categories.DoesNotExist:
        return Response({"Error": "No matching category"}, status=status.HTTP_404_NOT_FOUND)
    posts = Post.objects.filter(category=category)
    serializer_post = PostSerializer(posts, many=True)
    serializer_cat = CategorySerializer(category)
    return Response([serializer_cat.data, serializer_post.data], status=status.HTTP_200_OK)
