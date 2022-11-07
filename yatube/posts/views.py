"""Хранение представлений (контролеров) текущего приложения
Posts
"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render


from .models import Group, Post, User
from .forms import PostForm


def index(request):
    """Функция представления главной страницы проекта
    Yatube, с учётом сортировки количества постов для
    текущего приложения
    """
    template = 'posts/index.html'
    title = 'Это главная страница проекта Yatube'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.CONST_1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Функция представления страницы групп для проекта
    Yatube, с учётом сортировки количества постов для
    текущего приложения
    """
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, settings.CONST_1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    group_title = 'Здесь будет информация о группах проекта Yatube'
    context = {
        'group_title': group_title,
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    """Фунеция представления страницы пользователя"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, settings.CONST_1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'posts': posts,
        'author': user,
    }

    return render(request, template, context)


def post_detail(request, post_id):
    """Функция представления полной версии поста пользователя"""
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, username=post.author)
    count = Post.objects.filter(author=user).count()
    title = post.text[:settings.CONST_2]
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'title': title,
        'count': count,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Функция представления страницы создания нового поста"""
    if request.method == 'POST':

        form = PostForm(request.POST or None)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('posts:profile', request.user)

    form = PostForm()
    groups = Group.objects.all()
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'groups:': groups,
        'is_edit': False,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """Функция представления редактирования поста пользователя"""
    post = get_object_or_404(Post, pk=post_id)

    if not request.user == post.author:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            return redirect('posts:post_detail', post_id)

    form = PostForm(instance=post)
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
    }

    return render(request, template, context)
