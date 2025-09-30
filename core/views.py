
from django.shortcuts import render
from posts.models import Post


def index(request):
    posts = Post.objects.order_by('-created_at')[:4]
    return render(request, 'index.html', {'posts': posts})
