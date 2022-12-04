from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment
from .forms import CommentForm


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts})


def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
    num_of_comm = comments.count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data
            nickname = None
            author = None
            if request.user.is_authenticated:
                author = request.user
            elif request.user.is_anonymous and comment['nickname'] is not None:
                nickname = comment['nickname']
            # else:
            #     return HttpResponse(400)
            new_comment = Comment(text=comment['text'], post=post, author=author, nickname=nickname)
            print(new_comment)
            new_comment.save()
            return HttpResponseRedirect(f'/post/{pk}')
    else:
        form = CommentForm()
    return render(request, 'blog/post.html', {'post': post,
                                              'comments': comments,
                                              'num_of_comm': num_of_comm,
                                              'form': form,
                                              'user': request.user})


def get_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = CommentForm()
    return render(request, 'blog/post.html', {})
