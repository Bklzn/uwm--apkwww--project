from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Post, Comment
from .forms import CommentForm, PostForm


def index(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/index.html', {'posts': posts,
                                               'user': request.user})


def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk).order_by('-created_date')
    num_of_comm = comments.count()
    if request.method == 'POST':
        form = CommentForm(request.POST, is_authenticated=request.user.is_authenticated)
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
            new_comment.save()
            return HttpResponseRedirect(f'/post/{pk}')
    else:
        form = CommentForm()
    return render(request, 'blog/post.html', {'post': post,
                                              'comments': comments,
                                              'num_of_comm': num_of_comm,
                                              'form': form,
                                              'user': request.user})


def new_post(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data
            new_post = Post(text=post['text'], title=post['title'], published_date=post['published_date'], author=request.user)
            new_post.save()
            return HttpResponseRedirect(f'/post/{new_post.id}')
        return render(request, 'blog/new_post.html', {'form': form})
    else:
        return HttpResponse("Nie masz uprawnień, <a href='/api-authlogin'>zaloguj się</a>")


def profile(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('-published_date')
        posts_num = posts.count()
        comments = Comment.objects.filter(author=request.user).order_by("-created_date")
        comments_num = comments.count()
        return render(request, 'blog/profile.html', {'posts': posts, 'comments': comments})
    else:
        return HttpResponse("Nie masz uprawnień, <a href='/api-authlogin'>zaloguj się</a>")

