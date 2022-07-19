from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User

POSTS_ON_PAGE: int = 10


def create_pages(posts, request):
    """Разбиение постов на страницы."""
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


@cache_page(20, key_prefix='index_page')
def index(request):
    """Главная страница."""
    template = 'posts/index.html'
    posts = Post.objects.select_related('author', 'group')
    page_obj = create_pages(posts, request)
    return render(request, template, {'page_obj': page_obj})


def group_list(request, slug):
    """Страница группы."""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    page_obj = create_pages(group.posts.all(), request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Страница пользователя."""
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.all()
    if author.following.filter(author=author).all():
        following = True
    else:
        following = False
    page_obj = create_pages(posts_list, request)
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница поста."""
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    context = {
        'post': post,
        'form': CommentForm(),
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Страница создания поста."""
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', username=request.user)
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    """Страница редактирования поста."""
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    if post.id and request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'form': form,
        'is_edit': True,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    """Добавление комментария к посту."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """Страница подписок."""
    template = 'posts/follow.html'
    user = request.user
    posts = Post.objects.filter(author__following__user=user)
    page_obj = create_pages(posts, request)
    return render(request, template, {'page_obj': page_obj})


@login_required
def profile_follow(request, username):
    """Подписка на автора."""
    template = 'posts/follow.html'
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
    return render(request, template)


@login_required
def profile_unfollow(request, username):
    """Отписка от автора."""
    template = 'posts/unfollow.html'
    user = request.user
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=user, author=author).delete()
    return render(request, template, {'author': author})
