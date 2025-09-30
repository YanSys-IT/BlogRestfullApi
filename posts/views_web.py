from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import PostForm


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    from .forms import CommentForm
    comment_form = CommentForm()
    comment_error = None
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('web-post-detail', pk=post.pk)
        else:
            comment_error = "Пожалуйста, исправьте ошибки в комментарии."
    return render(request, 'posts/detail.html', {
        'post': post,
        'comment_form': comment_form,
        'comment_error': comment_error,
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('web-post-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/form.html', {'form': form, 'action': 'Создать пост'})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not request.user.is_staff:
        return redirect('web-post-detail', pk=post.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('web-post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'form': form, 'action': 'Редактировать пост'})
