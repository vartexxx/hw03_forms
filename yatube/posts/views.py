from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render


from .forms import PostForm
from .models import Group, Post, User


def get_default_context(stack, request):
    paginator = Paginator(stack, settings.CONST_1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj,
    }


def index(request):
    """Функция представления главной страницы проекта
    Yatube, с учётом сортировки количества постов для
    текущего приложения
    """
    template = 'posts/index.html'
    context = get_default_context(Post.objects.all(), request)
    return render(request, template, context)


def group_posts(request, slug):
    """Функция представления страницы групп для проекта
    Yatube, с учётом сортировки количества постов для
    текущего приложения
    """
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    context = {
        'group': group,
    }
    context.update(get_default_context(group.posts.all(), request))
    return render(request, template, context)


def profile(request, username):
    """Фунеция представления страницы пользователя"""
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    context = {
        'author': author,
    }
    context.update(get_default_context(author.posts.all(), request))
    return render(request, template, context)


def post_detail(request, post_id):
    """Функция представления полной версии поста пользователя"""
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'author': author,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    """Функция представления страницы создания нового поста"""
    form = PostForm(request.POST or None)
    context = {
        'form': form,
    }
    template = 'posts/create_post.html'
    if not form.is_valid():
        return render(request, template, context)
    new_post = form.save(commit=False)
    new_post.author = request.user
    new_post.save()
    return redirect('posts:profile', request.user)


@login_required
def post_edit(request, post_id):
    """Функция представления редактирования поста пользователя"""
    post = get_object_or_404(Post, pk=post_id)
    template = 'posts/create_post.html'
    if not request.user == post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    context = {
        'form': form,
        'post': post,
    }
    if not form.is_valid():
        return render(request, template, context)
    post = form.save()
    return redirect('posts:post_detail', post_id)
