from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm
from .models import Post, Group, Follow

User = get_user_model()


def index(request):
    """"Представление главной страницы постов"""
    post_list = Post.objects.order_by('-pub_date')
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, 10)
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Получаем набор записей для страницы с запрошенным номером
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    """"Представление страницы сообщества"""
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(
        Post.objects.filter(group=group).order_by('-pub_date'), 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {
        "group": group, "page": page})


@login_required
def new_post(request):
    """Представление формы новой записи"""
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("index")
    return render(request, "post_new.html", {
        'form': form, "post": None})


def profile(request, username):
    """"Представление страницы профайла"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts.order_by('-pub_date'), 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    number_of_posts = posts.count()
    following = Follow.objects.filter(
        user=request.user,
        author=user).exists() if request.user.is_authenticated else False
    context = {
        'author': user,
        'number_of_posts': number_of_posts,
        'page': page,
        'following': following,
        'profile': user
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    """"Представление страницы отдельного поста"""
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    comments = post.comments.select_related('author').all()
    context = {
        'form': form,
        'post': post,
        'author': post.author,
        'comments': comments
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    """"Представление страницы редактирования поста"""
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(
                "post",
                username=request.user.username,
                post_id=post_id)
    return render(
        request, 'post_new.html', {'form': form, 'post': post},
    )


def page_not_found(request, exception):
    """"Представление страницы 404"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """"Представление страницы 500"""
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    """"Функция для сохранения комментарий"""
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None, )
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list.order_by('-pub_date'), 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        'paginator': paginator
    }
    return render(request, "follow.html", context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username=username)
