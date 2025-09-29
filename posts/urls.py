from django.urls import path
from .views import PostListView, PostDetailView, add_comment

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),  # Список постов и создание
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Конкретный пост
    path('<int:post_id>/comments/', add_comment, name='add-comment'),  # Комментарии к посту
]
