from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from .models import Post


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})


def post(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, 'blog/post.html', {'post': post})
